# -*- coding:utf-8 -*-
import logging
from logging import handlers


class KGAlgoLogger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, output_screen=False, level='info', when='D', backCount=3,
                 fmt='%(asctime)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        self.logger.handlers.clear()
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别

        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器

        th.setFormatter(format_str)

        self.logger.addHandler(th)
