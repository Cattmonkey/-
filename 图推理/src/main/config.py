# -*- coding:utf-8 -*-

from tools.file_process import FileProcess
from tools.path import PathTools

KG_SOURCE_CONFIG = FileProcess.read_json(PathTools.PROJECT_ROOT + "data/config/config.json")
