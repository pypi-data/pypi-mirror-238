# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Author:       yunhgu
# Date:         2023/8/3
# -------------------------------------------------------------------------------
from .base import IO
from xmltodict import unparse, parse


class Xml(IO):
    @classmethod
    def read(cls, path) -> dict:
        """读取xml

        Args:
            path: xml路径

        Returns:
            字典xml内容
        """
        with open(path, encoding="utf-8", mode="r") as f:
            return parse(f.read(), encoding="utf-8")

    @classmethod
    def write(cls, path, content):
        """_summary_

        Args:
            path: xml路径
            content: 字典
        """
        with open(path, "w", encoding="utf-8") as f2:
            try:
                unparse(content, f2, pretty=True)
            except ValueError as v:
                unparse({"root": content}, f2, pretty=True)
                print(f"{path}:{v} and default add root for it")

    @staticmethod
    def name():
        """
        :return: string with name of geometry
        """
        return "xml"
