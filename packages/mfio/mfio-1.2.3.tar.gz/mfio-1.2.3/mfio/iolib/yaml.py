# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Author:       yunhgu
# Date:         2023/8/3
# -------------------------------------------------------------------------------
from .base import IO
from yaml import load, dump, SafeLoader, Dumper


# format the yaml
class MyDumper(Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


class Yaml(IO):
    @classmethod
    def read(cls, path) -> dict:
        with open(path, 'r', encoding='utf-8') as yaml_file:
            yaml_content = load(yaml_file, Loader=SafeLoader)
            return yaml_content

    @classmethod
    def write(cls, path, content):
        with open(path, 'w', encoding="utf-8") as f:
            dump(content, f, Dumper=MyDumper, default_flow_style=False, indent=4, allow_unicode=True)

    @staticmethod
    def name():
        """
        :return: string with name of geometry
        """
        return "yaml"
