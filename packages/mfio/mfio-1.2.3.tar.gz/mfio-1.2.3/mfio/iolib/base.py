# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Author:       yunhgu
# Date:         2023/8/3
# -------------------------------------------------------------------------------
class IO:
    @classmethod
    def read(cls,path):
        pass

    @classmethod
    def write(cls,path, content):
        pass

    @staticmethod
    def name():
        """
        :return: string with name of IO
        """
        raise NotImplementedError()
