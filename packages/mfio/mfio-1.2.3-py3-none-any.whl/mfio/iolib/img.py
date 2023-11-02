# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Author:       yunhgu
# Date:         2023/8/3
# -------------------------------------------------------------------------------
import cv2
from .base import IO
import numpy as np
from pathlib import Path


class Img(IO):
    @classmethod
    def read(cls, path) -> dict:
        return cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    @classmethod
    def write(cls, path, img_array):
        cv2.imencode(Path(path).suffix, img_array)[1].tofile(str(path))

    @staticmethod
    def name():
        """
        :return: string with name of geometry
        """
        return "image"
