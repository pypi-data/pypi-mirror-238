##
## High level API
##
##

from enum import Enum

from .enums import DBMTable, BLDCommandParameter, DBMAttributesVM

try:
    import davinsy_mms
    import davinsy_dbm
    import davinsy_bld
except ModuleNotFoundError as e:
    raise Exception(f"Cannot import C libs ({e})")


class LBL_ATTRIBUTE(Enum):
    DBM_ATT_LBL_LIST = 0x00


class DAT_ATTRIBUTE(Enum):
    DBM_ATT_DAT_META = 0x00
    DBM_ATT_DAT_DATA = 0x01


class SIG_ATTRIBUTE(Enum):
    DBM_ATT_SIG_SIGNATURE = 0x00
    DBM_ATT_SIG_OUTPUT_VEC = 0x01


class CTX_ATTRIBUTE(Enum):
    DBM_ATT_CTX = 0x00


class KEY_ATTRIBUTE(Enum):
    DBM_ATT_KEY = 0x00


class Row:

    def __init__(self, table, index, key=None):
        self.table = table
        self.index = index
        self.key = key

    def set_attribute(self, att, value):
        if isinstance(att, Enum):
            att = att.value
        if self.index >= 0 :
            add = davinsy_dbm.allocate_attribute(self.table.address, self.index, 0, att, len(value))
        else:
            add = davinsy_dbm.allocate_attribute(self.table.address, self.key, len(self.key), att, len(value))

        if add == 0:
            raise RuntimeError("Memory error "+str(len(value)) + " index "+str(self.index))
        davinsy_mms.write_to(add, value, len(value))

    def get_attribute(self, att):
        if isinstance(att, Enum):
            att = att.value
        (add, size) = davinsy_dbm.get_row(self.table.address, self.index, 0, att)
        return davinsy_mms.read_from(add, size)


class Table:

    def __init__(self, typ, address, nb_rows, row_size):
        self.typ = typ
        self.nb_rows = nb_rows
        self.row_size = row_size
        self.address = address

    def new_row(self, key):
        if key:
            return Row(self, davinsy_dbm.new_row(self.address, key, len(key)), key)
        else:
            return Row(self, davinsy_dbm.new_row(self.address, "", 0))

    def get_meta(self):
        meta = davinsy_dbm.get_meta(self.address)
        meta["table"] = DBMTable(meta["table"])
        return meta


def create_table(link,typ, nb_rows, row_size):
    if typ is None :
        raise Exception("typ of table NONE")

    if nb_rows is None :
        raise Exception("nb_rows NONE")

    if row_size is None :
        raise Exception("row_size NONE")
        
    if (nb_rows<1) :
        raise Exception("invalid nb_rows "+str(nb_rows))

    if (row_size<1) :
        raise Exception("invalid row_size "+str(row_size))
 
    return Table(typ,link.new_table(typ.value, nb_rows, row_size), nb_rows, row_size)


def get_table(type):
    if type == DBMTable.DBM_VM:
        return Table(type, davinsy_dbm.get(0x1000))
    elif type == DBMTable.DBM_LBL:
        return Table(type, davinsy_dbm.get(0x1001))
    elif type == DBMTable.DBM_DAT:
        return Table(type, davinsy_dbm.get(0x1002))
    elif type == DBMTable.DBM_KEY:
        return Table(type, davinsy_dbm.get(0x1003))

def compute_row_size(parts):
    rowsize = 0
    for p in parts:
        if p:
            rowsize += len(p)

    return rowsize


def alloc_mms_ring(size):
    return davinsy_mms.alloc(5,size)

def write_mms(add,value):
    barray = bytearray(value)
    davinsy_mms.write_to(add, barray, len(barray))

INDEX2ATTRIBUTE = (
    DBMAttributesVM.DBM_ATT_VM_DESC,
    DBMAttributesVM.DBM_ATT_VM_PREPROC_GRAPH_TRAIN,
    DBMAttributesVM.DBM_ATT_VM_PREPROC_GRAPH_INFER,
    # OTHER
    DBMAttributesVM.DBM_ATT_VM_DEEPLOMATH,
    DBMAttributesVM.DBM_ATT_VM_POSTPROC,
    DBMAttributesVM.DBM_ATT_VM_PREPROC_GRAPH_FEATURE_EXTRACTION,
    DBMAttributesVM.DBM_ATT_VM_PREPROC_GRAPH_BACKGROUND_AUGMENTATION,
    DBMAttributesVM.DBM_ATT_VM_PREPROC_GRAPH_DATA_AUGMENTATION,
)

def insert_row(table,label,parts):
    row = table.new_row(label)
    for i in range(len(parts)) :
        if not parts[i]:
            continue
        row.set_attribute(INDEX2ATTRIBUTE[i], parts[i])


def set_agent_id(agent_id):
    res = davinsy_bld.set(BLDCommandParameter.BLD_PARAM_AG_ID.value,bytearray(agent_id,encoding="ascii"))
    return res

def get_agent_id():
    agentid = davinsy_bld.get(BLDCommandParameter.BLD_PARAM_AG_ID.value)
    return agentid
