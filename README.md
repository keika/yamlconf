## config.yml - sample

```yaml
settings:
    encoding: "utf-8"
variables:
    pj_value1: "value1"
    pj_value2: "value2"
    pj_val_group:
        pj_value3: "value3"
        pj_list:
            "list1", "list2", "list3"
        pj_sub_group:
            pj_value4: "value4"
other_node1:
    input_dir:
        a_file: "${pj_value1}.txt"
        b_file: "%{os_env}/${pj_value2}.txt"
        c_file: "${pj_val_group.pj_value3}.txt"
```

## Sample using inheritance

```python
# conf.py
from yamlconf.config import Config
from os.path import abspath

class Conf(Config):
    in_a_file: str
    in_b_file: str
    out_z_file: str
    def __init__(self, config_path: str = "./config.yml"):
        super().__init__(config_path)
        self.in_a_file = abspath(self.nodes["other_node1"]["input_dir"]["a_file"])
        self.in_b_file = abspath(self.nodes["other_node1"]["input_dir"]["b_file"])
        self.out_z_file = abspath(self.nodes["other_node2"]["output_dir"]["z_file"])
```
```python
# __main__.py
from conf import Conf

def main():
    conf = Conf()
    print(conf.in_a_file)
    print(conf.in_b_file)
    print(conf.out_z_file)

if __name__ == "__main__":
    main()
```
