# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Author:       yunhgu
# Date:         2023/8/3
# -------------------------------------------------------------------------------
import csv
from .base import IO


class Csv(IO):
    @classmethod
    def read(cls, path) -> list:
        data_list = []
        with open(path, "r") as f:
            # 这里reader是一个生成器
            content = csv.reader(f)
            for row in content:
                data_list.append(row)
            return data_list

    @classmethod
    def write(cls, path, content):
        """
        :param file_path:生成文件路径
        :param content:csv内容 [(1, 2, 3), (4, 5, 6)]
        """
        with open(path, "w", newline='', encoding='cp936') as f:
            write = csv.writer(f)
            write.writerows(content)

    @staticmethod
    def name():
        """
        :return: string with name of geometry
        """
        return "csv"
