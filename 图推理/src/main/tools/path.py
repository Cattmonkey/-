# -*- coding:utf-8 -*-
import os
import shutil

"""
该模块下主要包含对路径及文件的操作
1）包含工程根目录
2）目录创建
3）目录删除
4）目录是否存在
5）文件是否存在
6）文件删除
"""


class PathTools:
    # 工程根目录
    PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../")

    @staticmethod
    def dir_is_exists(dirs):
        """
        判断文件或文件夹是否存在
        """
        if not os.path.exists(dirs):
            return False
        else:
            return True

    @staticmethod
    def makedirs(dirs):
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    @staticmethod
    def remove_and_makedirs(dirs):
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        else:
            shutil.rmtree(dirs)
            os.makedirs(dirs)

    @staticmethod
    def get_sub_dirs(dirs):
        temp = os.listdir(dirs)
        return [dirs + "/" + _ for _ in temp]

    @staticmethod
    def get_sub_dirs_name(dirs):
        temp = os.listdir(dirs)
        return temp

    @staticmethod
    def remove_dir(dirs):
        if os.path.exists(dirs):
            shutil.rmtree(dirs)

    @staticmethod
    def remove_file(file):
        if os.path.exists(file):
            os.remove(file)

    @staticmethod
    def copy_files(source, target):
        if not os.path.exists(target):
            shutil.copytree(source, target)


if __name__ == '__main__':
    a = PathTools.PROJECT_ROOT
    print(a)
