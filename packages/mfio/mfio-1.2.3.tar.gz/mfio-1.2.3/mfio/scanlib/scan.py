# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Author:       yunhgu
# Date:         2023/8/3
# -------------------------------------------------------------------------------
import os
from pathlib import Path
from collections import defaultdict


class Scan:
    """
    文件检索匹配
    """

    def __init__(self, path, suffixs: list = [".png", ".jpg", ".jpeg", ".bmp"], depth=2) -> None:
        self._path = path
        self._suffixs = suffixs
        self._depth = depth
        self._name_files = {}
        self._scan_files()

    @staticmethod
    def parent_name(file_path, parent_num=2):
        file_path = Path(file_path)
        return f"{'/'.join(file_path.parts[-parent_num:-1])}/{file_path.stem}"

    def _scan_files(self):
        for root, dirs, files in os.walk(self._path):
            for file in files:
                file_path = Path(os.path.join(root, file))
                if file_path.suffix in self._suffixs:
                    self._name_files[self.parent_name(file_path, self._depth)] = file_path

    def match_file(self, file, parent_num=2):
        return self._name_files.get(self.parent_name(file, parent_num))

    @property
    def file_list(self):
        return list(self._name_files.values())


if __name__ == '__main__':
    s = Scan(r"C:\Users\pc\Desktop\测试(4)\xml", suffixs=[".xml"], depth=1)
    a = r"C:\Users\pc\Desktop\测试(4)\图片\00ab97c54bb3459af2c659689b3ea643_50.jpg"
    print(s.match_file(a, 1))
    print(s.file_list)
