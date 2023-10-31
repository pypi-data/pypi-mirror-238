
def update_dict(default: dict, param: dict):
    """
    Update default value dict with new specific values
    Args:
        default: default value dict
        param: new / extra values dict
    """
    for key, value in param.items():
        if isinstance(value, dict):
            if key not in default:
                default[key] = {}
            update_dict(default[key], value)
        else:
            default[key] = param[key]


def get_params_with_default(defaultData: dict, parameters: dict, key: str):
    """
    Get default data from virtual model param dict and return these added values
    Args:
        defaultData: default parameters that can be overwritten
        parameters: parameters dict
        key: key to search in template
    Returns:
        paramDict: updated param dict with default value if needed
    """
    paramDict = defaultData.get(key, {})
    if key == "operations":
        paramDict = paramDict.get(parameters["typeid"], {})
    update_dict(paramDict, parameters)
    return paramDict
