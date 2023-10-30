from ai2_kit.core.util import load_yaml_file
from ruamel.yaml import YAML
import sys


class Yaml:
    def __init__(self) -> None:
        self.data = None

    def load(self, yaml_file: str):
        self.file = yaml_file
        self.data = load_yaml_file(yaml_file)
        return self

    def set_value(self, key: str, value):
        """edit a yaml file

        Args:
            yaml_file (str): path to the yaml file
            key (str): key to edit, support nested key, e.g. `a.b.c`
            value ([type]): new value
        """
        # TODO: handle missing key
        keys = key.split('.')
        d = self.data
        for k in keys[:-1]:
            d = d[k]
        d[keys[-1]] = value
        return self

    def dump(self, in_place = False):
        yaml = YAML()
        yaml.default_flow_style = False
        if in_place:
            with open(self.file, 'w') as fp:
                yaml.dump(self.data, fp)
        else: # to stdout
            yaml.dump(self.data, sys.stdout)
