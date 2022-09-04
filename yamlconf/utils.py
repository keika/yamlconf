import copy
import os
from . import const
import re

def load_values(multi_dic: dict)->dict:
    """_load_values

    Args:
        multi_dic (dict): config yaml -> dict

    Returns:
        dict: Expanded Variables
    """
    if const.VALS not in multi_dic.keys():
        return {}
    else:
        res = {}
        multid_to_flatd(multi_dic[const.VALS], res, "")
        return res

def load_settings(conf: dict)->dict:
    if const.SETS not in conf.keys():
        return {}
    else:
        return copy.deepcopy(conf[const.SETS])

def load_other_nodes(conf: dict)->dict:
    res = {}
    for k in conf.keys():
        if k not in [const.VALS, const.SETS]:
            res[k] = conf[k]
    return copy.deepcopy(res)

def multid_to_flatd(multi_dic: dict, container: dict[str, str], base_name: str)->None:
    """_multid_to_flatd

    Args:
        multi_dic (dict): config yaml -> dict
        container (dict[str, str]): store variables
        base_name (str): Base name of high-level variable names joined by periods.
    """
    for k in multi_dic.keys():
        key = f"{base_name}.{k}" if base_name != "" else k
        if type(multi_dic[k]) == dict:
            multid_to_flatd(multi_dic[k], container, key)
        else:
            container[key] = multi_dic[k]
    
def env_replace(target: str, vals: dict, strict: bool = True)->str:
    res = target
    for m in re.finditer(r"\$\{(?P<name>[\w\.]+?)\}", res):
        key = m.group("name")
        if key in vals.keys():
            res = res.replace("${"+key+"}", vals[key])
        else:
            if strict:
                raise Exception(f"The specified key is not found [config_val:{key}]")
    for m in re.finditer(r"\%\{(?P<name>[\w]+?)\}", res):
        key = key = m.group("name")
        e_val = os.getenv(key)
        if e_val:
            res = res.replace("%{"+key+"}", e_val)
        else:
            if strict:
                raise Exception(f"The specified key is not found [os_env:{key}]")
    return res

def dict_replace(target: dict, vals: dict)->None:
    t = target
    for key in t.keys():
        v_type = type(t[key])
        if v_type == dict:
            dict_replace(t[key], vals)
        elif v_type == str:
            t[key] = env_replace(t[key], vals)
    
            