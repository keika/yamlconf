from distutils.command.config import config
from os import stat
from typing import overload
import yaml
from . import const
from . import utils
from os.path import abspath

class Config:
    """config class
    
    self.encondig str:
        config.yaml - /settings/encoding
        
    self._settings dict:
        config.yaml - /settings
    
    self._path str:
        Path of the yaml file that was loaded
    
    self._raw str:
        config.yaml - /
    
    self.variables dict:
        config.yaml - /variables
        Variables in the value section have been expanded.
    
    self.nodes dict:
        config.yaml - Nodes other than /setting or /variables
    
    """
    encoding: str
    _settings: dict
    _path: str
    _raw: dict
    variables: dict
    nodes: dict
    def __init__(self, config_path: str = "./config.yml"):
        self._path = abspath(config_path)
        with open(self._path) as f:
            self._raw = yaml.safe_load(f)
        self.variables = vals = utils.load_values(self._raw)
        utils.dict_replace(vals, vals)
        
        self._settings = utils.load_settings(self._raw)
        self.encoding = self._settings[const.ENCODING]
        
        self.nodes = utils.load_other_nodes(self._raw)
        utils.dict_replace(self.nodes, vals)
