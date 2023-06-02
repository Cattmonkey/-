# -*- coding:utf-8 -*-
import json
import traceback
"""
该模块提供知识图谱构建-算法的异常类
"""


class ParamError(Exception):
    """
    解析参数异常
    """
    pass


class GetDataError(Exception):
    """
    获取数据异常
    """
    pass


class PutDataError(Exception):
    """
    输出数据异常
    """
    pass


class DataPreProcessError(Exception):
    """
    数据预处理异常
    """
    pass


class TrainError(Exception):
    """
    训练过程异常
    """
    pass


class SaveModelError(Exception):
    """
    模型保存异常
    """
    pass


class PredictError(Exception):
    """
    预测过程异常
    """
    pass


class ComputeError(Exception):
    """
    预测过程异常
    """
    pass


class MessageCode:
    # 1)正常情况
    class NormalCode:
        normal = 0

    # 2)参数异常
    class ParamErrorCode:
        error_code = 1000

    class GetDataErrorCode:
        error_code = 2000

    class PutDataErrorCode:
        error_code = 3000

    class DataPreProcessErrorCode:
        error_code = 4000

    class TrainErrorCode:
        error_code = 5000

    class SaveModelErrorCode:
        error_code = 6000

    class PredictErrorCode:
        error_code = 7000

    class AlgoSystemErrorCode:
        error_code = 9000


class ExceptionReturn:
    def __init__(self, code="", message="", data=None):
        self.code = code
        self.message = message
        self.data = data

    def info(self):
        info = {"code": self.code, "message": self.message, "data": self.data}
        return json.dumps(info, ensure_ascii=False)

class KGAlgoException(Exception):
    def __init__(self, code="", message="", data=None):
        self.code = code
        self.message = message
        self.data = data

    def info(self):
        info = {"code": self.code, "message": self.message, "data": self.data}
        return json.dumps(info, ensure_ascii=False)


if __name__ == '__main__':

    try:
        try:
            try:
                a = []
                print(a[1])
            except Exception as e:
                # raise ParamError("ljljklkljkl,%s" % traceback.format_exc())
                raise ParamError("里面")

        except Exception as e:
            raise ParamError("ljljklkljkl")
            # raise e
        pass
    except Exception as e:
        traceback.print_exc()
        a = traceback.format_exc()
        pass

