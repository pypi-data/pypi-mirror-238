# Management of virtual models data

import yaml
from enum import Enum
from pathlib import Path
from ctypes import c_uint, c_ubyte, c_float, c_int, c_ushort, Array
from ctypes import Union, Structure, sizeof


from . import utils
from .operations import CUST_OP, CALLPARAMS, fill_params
from .enums import PPOperationUID
from .logger import logger

try:
    import davinsy_run
except ModuleNotFoundError as e:
    raise Exception(f"Cannot import C libs ({e})")

# ---- UID MGMT ----

_Structure = type("Structure", (Structure,), {})
_Union = type("Union", (Union,), {})

def get_Structure():  
    return _Structure

def get_Union():
    return _Union

# ---- VM ATTRIBUTES ----


class CATTSTRING(get_Structure()):
    _fields_ = [
        ("length", c_ubyte),
        ("string", c_ubyte * 16)
    ]


class CROWID(get_Union()):
    _fields_ = [
        ("key", c_ubyte * 16),
        ("index", c_uint)
    ]


class CATTROWID(get_Structure()):
    _pack_ = True
    _fields_ = [
        ("length", c_ubyte),
        ("id", CROWID)
    ]


class CFILTERELT(get_Structure()):
    _fields_ = [
        ("key", CATTROWID),
        ("nb_labels", c_ubyte),
        ("labels", 5 * c_ubyte)
    ]


class CFILTER(get_Structure()):
    _fields_ = [
        ("max_row", c_uint),
        ("mode", c_ushort),
        ("nb_filters", c_ubyte),
        ("filters", 5 * CFILTERELT)
    ]


class CDescription(get_Structure()):
    _pack_ = True
    _fields_ = [
        ("description", CATTSTRING),
        ("axis", CATTROWID),
        ("split", CATTROWID),
        ("maxsplit",c_uint),
        ("reduction", (4* c_uint)),
        ("filter", CFILTER)
    ]


class CMEMNEED(get_Structure()):
    _fields_ = [
        ("outlen", c_uint),
        ("templen", c_uint)
    ]


class CGRAPHNODE(get_Structure()):
    _pack_ = True
    _fields_ = [
        ("operation_id", c_uint),
        ("memneed", CMEMNEED),
        ("mem_policy", c_uint),
        ("nb_next", c_uint),
        ("next", 14 * c_ubyte),
        ("parameters", CALLPARAMS)
    ]

    def get_parameters(self,opuid):
        # LEGACY
        if opuid == PPOperationUID.OPS_UID_MFCC2048F32.value:
            return self.parameters.param_mfcc
        elif opuid == PPOperationUID.OPS_UID_PWSPANF32.value:
            return self.parameters.param_pwspan
        elif opuid == PPOperationUID.OPS_UID_NOISEMIXF32.value:
            return self.parameters.param_noisemix
        elif opuid == PPOperationUID.OPS_UID_CP1D.value:
            return self.parameters.param_mode
        elif opuid == PPOperationUID.OPS_UID_RESHAPEF32.value:
            return self.parameters.param_mode
#        elif opuid == PPOperationUID.OPS_UID_DCT2D.value:
#            return self.parameters.param_dct2d
        else:
            if (opuid >= CUST_OP.OP_CUST_FIRST.value):
                return self.parameters.param_mode        
            else:
                raise RuntimeError("Operation not yet supported")


def preprocgraph_factory(nb):
    class CPreprocGraph(Structure):
        _pack_ = True
        _fields_ = [
            ("nb", c_uint),
            ("memneed", CMEMNEED),
            ("sizeout", c_uint),
            ("nodes", nb * CGRAPHNODE),
        ]

    return CPreprocGraph


class CDeeplomath(get_Structure()):
    _fields_ = [
        ("dim_in", c_uint),
        ("dim_out", c_uint),
        ("max_rows", c_uint),
        ("max_layers", c_uint),
        ("distancefunc", c_uint),
        ("nbInstances", c_uint),
        ("mode", c_int),
        ("rejection", c_int),
    ]


class CPostProc(get_Structure()):
    _fields_ = [
        ("op", c_uint),
        ("ringbufferdepth", c_uint),
        ("ringbufferwidth", c_uint),
        ("reserved", c_uint),
        ("mode", c_int),
        ("rejection", c_int),
    ]


# ---- DAT ATTRIBUTES ----


class CMETALABEL(get_Structure()):
    _pack_ = True
    _fields_ = [
        ("id", CATTROWID),
        ("label", c_ubyte)
    ]


def CMeta_factory(type, n):
    if type == 0:
        dataType = CMETALABEL
        key = "labels"
    else:
        dataType = c_float
        key = "values"

    class CMeta(get_Structure()):
        _pack_ = True
        _fields_ = [
            ("type", c_ushort),
            ("qi", c_ushort),
            (key, n * dataType)
        ]

    return CMeta


# ---- UTILS ----

def tuple2rowid(t: tuple) -> CROWID:
    """
    transform a tuple in the yaml to a row_id_t structure
    Args:
        t: the tuple
    Returns:
        the ctypes row_id_t
    """
    if t[0] == 0:
        row_id = CROWID(index=t[1])
    elif t[1] is None:
        row_id = CROWID(index=0)
    else:
        row_id = CROWID(key=t[1])
    return row_id


def tuple2attrowid(t: tuple) -> CATTROWID:
    """
    transforms a tuple in the yaml to a dbm_att_row_id_t
    Args:
        t: the tuple
    Returns:
        the ctypes dbm_att_row_id_t
    """
    return CATTROWID(length=t[0], id=tuple2rowid(t))


def string2bytearray(size: int, s: str) -> Array:
    """
    Transforms a python string to an array of bytes
    Args:
        size: The size of the final array
        s: the string to transform
    Returns:
        a ctypes array of byte
    """
    return (c_ubyte * size)(*[int(b) for b in bytes(s, "ascii")])

class PreprocPhase(Enum):
    """
    Enum to define the different possible preprocessing phases
    need to be sync with dexim (VM generation), maybe needs to be in enums.py
    """
    TRAINING = "train"
    INFERENCE = "infer"
    OTHER = "other" 
    FEATURE_EXTRACTION = "feature_extraction"
    DATA_AUGMENTATION = "data_augmentation"
    BACKGROUND_ADAPTATION = "background_adaptation"
    DATA_TRANSFORM = "data_transform"

class VirtualModel:
    """
    This class describes a virtual model
    """
    id2uid = {}
    
    def __init__(self, path: Path, templatePath: Path):
        with open(path, 'r') as file:
            self.model = yaml.safe_load(file)["model"]
#        with open(templatePath / "template.yml", 'r') as file:  # FIXME : why several templates?
#            self.defaultData = yaml.safe_load(file)
        self.defaultData ={} 

        self.uid2id = {}

    def set_agent(self,agent):
        self.agent = agent

    def set_uid2id(self,uid_list):
        for id in range(0,len(uid_list)):
            self.id2uid[id] = uid_list[id] 

    def convert_id2uid(self,id):
        if (id >= CUST_OP.OP_CUST_FIRST.value):
            return id
        
        if id in self.id2uid:
            return self.id2uid[id]
        raise Exception(f" ERROR can not convert operation id {id}")

    def convert_uid2id(self,uid):
        if (uid >= CUST_OP.OP_CUST_FIRST.value):
            return uid

        for id,uid_tmp in self.id2uid.items():
            if uid_tmp == uid:
                return id
        raise Exception(f" ERROR can not convert operation uid {uid}")

    def get_name(self):
        return self.model["description"]["name"]

    def get_bootstrap_info(self):
        if "bootstrap" in self.model:
            return self.model["bootstrap"]
        return None

    def _update_node_sizes(self, level, graph, index, previous):
		# DEPRECATED
        node = graph.nodes[index]
        uid = self.convert_id2uid(node.operation_id)
        coutlen = node.get_parameters(uid).get_out_len(previous,uid)
        ctmplen = node.get_parameters(uid).get_temp_len(previous,uid)

        if node.memneed.outlen == 0:
            node.memneed.outlen = int(coutlen)

        if node.memneed.templen == 0:
            node.memneed.templen = int(ctmplen)

        logger.debug("\t" * level + "%08x" % uid)
        logger.debug("\t" * level + "\toutlen %d" % node.memneed.outlen)
        logger.debug("\t" * level + "\ttmplen %d" % node.memneed.templen)

        maxout = 0
        maxtmp = 0

        if node.nb_next==0:
            sizeout = node.memneed.outlen
        else:
            sizeout = 0
            for i in range(node.nb_next):
                if i == 0 : # it's the root => out data of the preproc
                    sizeout += node.memneed.outlen
                else:
                    uid = self.convert_id2uid(node.operation_id)
                    (outlen, templen,sout) = self._update_node_sizes(level + 1, graph, node.next[i], node.get_parameters(uid))
                    maxout = max(outlen, maxout)
                    maxtmp = max(templen, maxtmp)
                    sizeout += sout

        return coutlen + maxout, max(ctmplen, maxtmp), sizeout

    def _update_graph_sizes(self, graph):
        (outlen, templen, sizeout) = self._update_node_sizes(0, graph, 0, None)

        if (graph.memneed.outlen == 0):
            graph.memneed.outlen = int(outlen)

        if (graph.memneed.templen == 0):
            graph.memneed.templen = int(templen)

        if (graph.sizeout == 0):
            logger.debug("graph.sizeout overwrite with %d "% (sizeout))
            graph.sizeout = int(sizeout)

        logger.debug("-> graph outlen; %d, templen %d, sizeout %d" % (graph.memneed.outlen, graph.memneed.templen, graph.sizeout))


    def maxsplitdefault(self,desc):
        if "maxsplit" in desc :
            maxsplit=(desc["maxsplit"])
        else :
            maxsplit = (1)
        return maxsplit

    def get_C_description(self):
        desc = utils.get_params_with_default(self.defaultData, self.model["description"], "description")
        logger.debug(" DESC :"+ str(desc))
        filt = desc["filter"]

        return CDescription(
            description=CATTSTRING(len(desc["description"]), string2bytearray(16, desc["description"])),
            axis=tuple2attrowid(desc["axis"]),
            split=tuple2attrowid(desc["split"]),
            maxsplit = self.maxsplitdefault(desc),
            reduction= (4* c_uint)(*desc["reduction"]), #             [0,0,0,0] # active / dummies / garbage / reserved
            filter=CFILTER(
                maxrow=filt["max_row"],
                mode=filt["mode"],
                nb_filters=len(filt["filters"]),
                filters=(5 * CFILTERELT)(
                    *[
                        CFILTERELT(
                            key=tuple2attrowid(f["key"]),
                            nb_labels=len(f["labels"]),
                            labels=f["labels"],
                        ) for f in filt["filters"]
                    ]
                )
            ),
        )

    def get_msgpack_description(self):
        desc = utils.get_params_with_default(self.defaultData, self.model["description"], "description")
        filt = desc["filter"]
        axis = desc["axis"]
        split = desc["split"]

        
        #description
        arr = [
            desc["description"],
        ]

        #axis
        if axis[0] != 0:
            arr.append(axis[1])
        else:
            arr.append("")
            arr.append(axis[1])
        
        #split
        if split[0] == 0 :
            arr.append("")
            arr.append(split[1])
        elif split[0] == 0xFF:
            arr.append("")
            arr.append(-1)
        else:
            arr.append(split[1])

        #maxsplit
        arr.append(self.maxsplitdefault(desc))

        #reduction
        arr.append(desc["reduction"])

        #filter
        arr.append(filt["max_row"])
        arr.append(filt["mode"])
        flt_arr = []
        for f in filt["filters"]:
            if f["key"][0] == 0:
                flt_arr.append("")
                flt_arr.append(f["key"][1])
            else:
                flt_arr.append(f["key"][1])
            flt_arr.append(f["labels"])
        arr.append(flt_arr)

        logger.debug("MSGPACK description %s" % arr)

        return arr
    def cast_memneed (self,memneed):

        memneedFields = CMEMNEED._fields_
        for (field, typeField) in memneedFields:            
            if field in memneed:
                if typeField == c_int or typeField == c_uint:
                    try :
                        if memneed[field] != int(memneed[field]):
                            raise TypeError(f"memneed {field} is not an integer")
                        memneed[field] = int(memneed[field])
                    except TypeError :
                        raise TypeError(f"memneed {field} incorrect type with {memneed[field]}")
                    except ValueError :
                        raise ValueError(f"memneed {field} incorrect value : {str(memneed[field])}")
                    except Exception as e :
                        raise ValueError(f"memneed {field} exception for : {str(memneed[field])}")
                # else : # float point testing

            else:
                raise TypeError(f"memneed {field} is mandatory and not found")

        return memneed
    def cast_preproc (self,preproc):

        memneed = preproc["memneed"]
        preproc["memneed"] = self.cast_memneed(memneed)

        for n in preproc["nodes"]:
            memneed = n["memneed"]
            n["memneed"] = self.cast_memneed(memneed)

        preproc["sizeout"] = int(preproc["sizeout"])

        return preproc

    def get_C_preproc(self, phase):

        if not phase in self.model["preprocess"]:
            return None
        
        preproc = self.model["preprocess"][phase]
        
        # TODO: check all the graph
        preproc = self.cast_preproc(preproc)

        graph = preprocgraph_factory(len(preproc["nodes"]))(
            nb=len(preproc["nodes"]),
            memneed=CMEMNEED(preproc["memneed"]["outlen"], preproc["memneed"]["templen"]),
            sizeout=preproc["sizeout"],
            nodes=(CGRAPHNODE * len(preproc["nodes"]))(*[
                CGRAPHNODE(
                    operation_id=self.convert_uid2id(n["operation_id"]),
                    memneed=CMEMNEED(
                        n["memneed"]["outlen"],
                        n["memneed"]["templen"],
                    ),
                    mem_policy=n["mem_policy"],
                    nb_next=len(n["next"]),
                    next=(14 * c_ubyte)(*n["next"]),
                    parameters=fill_params(self.defaultData, n["parameters"])
                )
                for n in preproc["nodes"]])
        )

        # self._update_graph_sizes(graph) # LEGACY
        return graph
    def get_C_preproc_size(self, phase):
        
        size = 0

        if not phase in self.model["preprocess"]:
            phaselist = self.model["preprocess"].keys()
            logger.debug(f"phase {phase} not in {phaselist}")
        else: 
            preproc = self.model["preprocess"][phase]
            
            preproc = self.cast_preproc(preproc)

            graph = preprocgraph_factory(len(preproc["nodes"]))(
                nb=len(preproc["nodes"]),
                memneed=CMEMNEED(preproc["memneed"]["outlen"], preproc["memneed"]["templen"]),
                sizeout=preproc["sizeout"],
                nodes=(CGRAPHNODE * len(preproc["nodes"]))(*[
                    CGRAPHNODE(
                        operation_id=0, #don't care about the operation_id
                        memneed=CMEMNEED(
                            n["memneed"]["outlen"],
                            n["memneed"]["templen"],
                        ),
                        mem_policy=n["mem_policy"],
                        nb_next=len(n["next"]),
                        next=(14 * c_ubyte)(*n["next"]),
                        parameters=fill_params(self.defaultData, n["parameters"])
                    )
                    for n in preproc["nodes"]])
            )

            if graph is not None:
                size = len(bytearray(graph))
        return size
    
    def get_msgpack_preproc(self, phase):

        # we need to get the graph with computed values
        # from the model
        graph = self.get_C_preproc(phase)

        arr = [
            graph.memneed.outlen,
            graph.memneed.templen,
            graph.sizeout,
        ]

        arr_nodes = [
        ]

        for i in range(graph.nb):
            arr_nodes.append([
                graph.nodes[i].operation_id,
                graph.nodes[i].memneed.outlen,
                graph.nodes[i].memneed.templen,
                graph.nodes[i].mem_policy,
                [graph.nodes[i].next[j] for j in range(graph.nodes[i].nb_next)],
                graph.nodes[i].parameters.param.typeid,
                graph.nodes[i].parameters.param.size,
                [bytearray(graph.nodes[i].parameters.param.data),],
            ])

        arr.append(arr_nodes)

        logger.debug("MSGPACK preproc %s" % arr)

        return arr 
    def cast_dlm (self,dlm):
        dlmFields = CDeeplomath._fields_
        for (field, typeField) in dlmFields:            
            if field in dlm:
                if typeField == c_int or typeField == c_uint:
                    try :
                        if dlm[field] != int(dlm[field]):
                            raise TypeError(f"Deeplomath {field} is not an integer")
                        dlm[field] = int(dlm[field])
                    except TypeError :
                        raise TypeError(f"Deeplomath {field} incorrect type with {dlm[field]}")
                    except ValueError :
                        raise ValueError(f"Deeplomath {field} incorrect value : {str(dlm[field])}")
                    except Exception as e :
                        raise ValueError(f"Deeplomath {field} exception for : {str(dlm[field])}")
                # else : # float point testing

            else:
                raise TypeError(f"Deeplomath {field} is mandatory and not found")

        return dlm
    def get_C_deeplomath(self):
        dlm = utils.get_params_with_default(self.defaultData, self.model["deeplomath"], "deeplomath")
        dlm = self.cast_dlm(dlm)
        logger.debug(" DLM "+str(dlm))
        res = CDeeplomath(**dlm)

        return res

    def get_msgpack_deeplomath(self):
        dlm = utils.get_params_with_default(self.defaultData, self.model["deeplomath"], "deeplomath")

        arr = [
            dlm["dim_in"],
            dlm["dim_out"],
            dlm["max_rows"],
            dlm["max_layers"],
            dlm["distancefunc"],
            dlm["nbInstances"],
            dlm["mode"],
            dlm["rejection"],
        ]

        return arr



    def get_C_postproc(self):
        pst = self.model["postprocess"]

        logger.debug("POSTPROC ", pst)

        res = CPostProc(**pst)

        return res

    def get_msgpack_postproc(self):
        pst = self.model["postprocess"]

        arr = [
            pst["op"],
            pst["ringbufferdepth"],
            pst["ringbufferwidth"],
            pst["reserved"],
            pst["mode"],
            pst["rejection"],
        ]

        return arr

    def get_parts(self):
        desc = None
        preproc_train = None
        preproc_infer = None
        deeplomath = None
        postproc = None
        if "description" in self.model:
            desc = bytearray(self.get_C_description())
        
        if "preprocess" in self.model:
            if "train" in self.model["preprocess"]:
                preproc_train = bytearray(self.get_C_preproc("train"))
            if "infer" in self.model["preprocess"]:
                preproc_infer = bytearray(self.get_C_preproc("infer"))
        if "deeplomath" in self.model:
            deeplomath = bytearray(self.get_C_deeplomath())
        if "postprocess" in self.model:
            postproc = bytearray(self.get_C_postproc())

        return (desc,preproc_train,preproc_infer,deeplomath,postproc)


    def get_model(self):
        return self.model
        
    def get_deeplomath(self):
        return self.model["deeplomath"]


    def get_vm_row_size(self) -> int:
        """
        Load th Virtual Model to DavinSy
        """
        # Get the C version of it
        desc = bytearray(self.get_C_description())
        deeplomath = bytearray(self.get_C_deeplomath())
        postproc = bytearray(self.get_C_postproc())

        # access to preproc from python
        preprocSize = 0
        for preprocPhase in PreprocPhase:
            preproc_c_size = self.get_C_preproc_size(preprocPhase.value)
            if preproc_c_size is None or preproc_c_size == 0 :
                # logger.warn("Preproc of type %s not present in the VM" % preprocPhase.name)
                continue
            if preprocPhase.value == PreprocPhase.FEATURE_EXTRACTION.value:
                # multiply by 2 for TRAIN & INFER
                preproc_c_size = 2*preproc_c_size

            preprocSize += preproc_c_size

        # Creating the Virtual Model table at the good size
        rowsize = len(desc) + preprocSize + len(deeplomath) + len(postproc)
        return rowsize

# DBM Utils
# It's in this file because it needs the CMeta_factory

def compute_dbm_row_size_class(rawDataMaxLen,maxLabels) -> int:

    size = sizeof(CMeta_factory(0, maxLabels)) + rawDataMaxLen * 4
    return size
    
def compute_dbm_row_size_reg(rawDataMaxLen,maxRegLen) -> int:

    size = sizeof(CMeta_factory(0, maxRegLen)) + rawDataMaxLen * 4
    return size


def compute_ctx_row_size():
    sizeof_DLM_ENV = 1536

    return sizeof_DLM_ENV
