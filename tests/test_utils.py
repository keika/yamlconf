import copy
import pytest
import os
from yamlconf import utils

@pytest.fixture(scope="module")
def config_data():
    d = {
        "settings": {
            "encoding": "utf-8"
        },
        "variables": {
            "pj_value1": "value1",
            "pj_value2": "value2",
            "pj_val_group": {
                "pj_value3": "value3",
                "pj_list": ["list1", "list2", "list3"],
                "pj_sub_group": {
                    "pj_value4": "value4"
                }
            },
            "pj_val_rep": "${pj_value1}",
        },
        "other_node1": {
            "input_dir": {
                "a_file": "${pj_value1}.txt",
                "b_file": "%{os_env}/${pj_value2}.txt",
                "c_file": "${pj_val_group.pj_value3}.txt",
            },
        },
        "other_node2": {
            "output_dir": {
                "z_file": "./output.txt"
            },
        },
    }
    yield d

def test_load_values(config_data):
    values = utils.load_values(config_data)
    assert values["pj_value1"] == "value1"
    assert values["pj_value2"] == "value2"
    assert values["pj_val_group.pj_value3"] == "value3"
    assert values["pj_val_group.pj_list"][1] == "list2"
    assert values["pj_val_group.pj_sub_group.pj_value4"] == "value4"
    assert values["pj_val_rep"] == "${pj_value1}"

def test_env_replace():
    d = {
        "rep_key1": "|value1|",
        "rep_key2.sub_key2": "|value2|"
    }
    os.environ["OS_ENV"] = "|ENV_VAL|"
    assert utils.env_replace("aaa${rep_key1}bbb${rep_key2.sub_key2}ccc", d) == "aaa|value1|bbb|value2|ccc"
    assert utils.env_replace("aaa%{os_env}bbb${rep_key1}", d) == "aaa|ENV_VAL|bbb|value1|"
    with pytest.raises(Exception) as e:
        utils.env_replace("aaa${exception}bbb", d)
    assert str(e.value).startswith("The specified key is not found [config_val:")
    with pytest.raises(Exception) as e:
        utils.env_replace("aaa%{exception}bbb", d)
    assert str(e.value).startswith("The specified key is not found [os_env:")

def test_dict_replace(config_data):
    values = utils.load_values(config_data)
    utils.dict_replace(values, values)
    assert values["pj_value1"] == "value1"
    assert values["pj_value2"] == "value2"
    assert values["pj_val_group.pj_value3"] == "value3"
    assert values["pj_val_group.pj_list"][1] == "list2"
    assert values["pj_val_group.pj_sub_group.pj_value4"] == "value4"
    assert values["pj_val_rep"] == "value1"


def test_dict_replace_multi_structure(config_data):
    values = utils.load_values(config_data)
    node = copy.deepcopy(config_data["other_node1"])
    os.environ["OS_ENV"] = "ENV_VAL"
    utils.dict_replace(node, values)
    assert node["input_dir"]["a_file"] == "value1.txt"
    assert node["input_dir"]["b_file"] == "ENV_VAL/value2.txt"
    assert node["input_dir"]["c_file"] == "value3.txt"

def test_load_other_nodes(config_data):
    nodes = utils.load_other_nodes(config_data)
    assert "variables" not in nodes.keys()
    assert "other_node1" in nodes.keys()
    assert "other_node2" in nodes.keys()