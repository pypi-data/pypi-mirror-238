# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Author:       yunhgu
# Date:         2023/8/3
# -------------------------------------------------------------------------------
from .base import IO


class Text(IO):
    @classmethod
    def read(cls, path)->list:
        with open(path, mode='r', encoding="utf-8") as f:
            return f.readlines()

    @classmethod
    def write(cls, path, content):
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def name():
        """
        :return: string with name of geometry
        """
        return "text"
