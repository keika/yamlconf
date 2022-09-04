import pytest
import os
from yamlconf.config import Config
from os.path import abspath


def test_config_init():
    os.environ["os_env"] = "env_value"
    config = Config("./tests/data/config.yml")
    assert config.encoding == "utf-8"
    assert config.variables["pj_val_rep"] == "value1"
    assert config.nodes["other_node1"]["input_dir"]["b_file"] == "env_value/value2.txt"

class InheritanceConfig(Config):
    in_a_file: str
    in_b_file: str
    out_z_file: str
    def __init__(self, config_path: str = "./config.yml"):
        super().__init__(config_path)
        self.in_a_file = abspath(self.nodes["other_node1"]["input_dir"]["a_file"])
        self.in_b_file = abspath(self.nodes["other_node1"]["input_dir"]["b_file"])
        self.out_z_file = abspath(self.nodes["other_node2"]["output_dir"]["z_file"])
        
def test_inheritance_config():
    os.environ["os_env"] = "pytest_dir"
    config = InheritanceConfig("./tests/data/config.yml")
    base = os.getcwd()
    assert config.in_b_file == os.path.join(base, "pytest_dir", "value2.txt")
    assert config.out_z_file == os.path.join(base, "output.txt")