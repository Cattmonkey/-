# -*- coding:utf-8 -*-
import json

"""
文件处理
"""

class FileProcess:
    @staticmethod
    def save_json(data, save_path):
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    @staticmethod
    def read_json(read_path):
        with open(read_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
