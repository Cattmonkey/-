# -*- coding:utf-8 -*-
import argparse
import json

from .error import KGAlgoException, MessageCode

parser = argparse.ArgumentParser(description='Net Compute')

parser.add_argument('--port', default="5000", help='running port', type=str)


def params_check(params):
    if "task_type" not in params.keys() or params["task_type"] not in ["train", "predict"]:
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="输入参数必须包含合法的任务类型参数!")

    if params["task_type"] == "train":
        if "training_model_root_path" not in params.keys() or params["training_model_root_path"] == "None" or \
                params[
                    "training_model_root_path"] is None:
            raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="训练模式下必须输入合法的模型根路径，请检查！!")

        if "training_model_name" not in params.keys() or params["training_model_name"] == "None" or params[
            "training_model_name"] is None:
            raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="训练模式下必须输入合法的模型名称，请检查！!")
        if "training_model_version" not in params.keys() or params["training_model_version"] == "None" or params[
            "training_model_version"] is None:
            raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="训练模式下必须输入合法的模型版本号，请检查！!")
        if "training_incremental_model_version" not in params.keys() or params[
            "training_incremental_model_version"] == "None" or params[
            "training_incremental_model_version"] is None:
            raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="训练模式下必须选择是否增量训练，请检查！!")
        if "training_corpus_root_path" not in params.keys() or params[
            "training_corpus_root_path"] == "None" or params[
            "training_corpus_root_path"] is None:
            raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="训练模式下必须输入合法的训练语料根路径，请检查！!")
        if "training_corpus_name" not in params.keys() or params[
            "training_corpus_name"] == "None" or params[
            "training_corpus_name"] is None:
            raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="训练模式下必须输入合法的训练语料库名称，请检查！!")

        if "training_params" not in params.keys() or params[
            "training_params"] == "None" or params[
            "training_params"] is None:
            raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="训练模式下必须输入合法的模型训练参数，请检查！!")
        else:
            check_train_params(params["training_params"])

    if params["task_type"] == "predict":

        if "prediction_model_root_path" not in params.keys() or params[
            "prediction_model_root_path"] == "None" or params[
            "prediction_model_root_path"] is None:
            raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="预测模式下必须输入合法的训练语料根名称，请检查！!")
        if "prediction_model_root_path" not in params.keys() or params[
            "prediction_model_root_path"] == "None" or params[
            "prediction_model_root_path"] is None:
            raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="预测模式下必须输入合法的模型路径，请检查！!")

        if "prediction_model_name" not in params.keys() or params[
            "prediction_model_name"] == "None" or params[
            "prediction_model_name"] is None:
            raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="预测模式下必须输入合法的模型名称，请检查！!")

        if "prediction_model_version" not in params.keys() or params[
            "prediction_model_version"] == "None" or params[
            "prediction_model_version"] is None:
            raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="预测模式下必须输入合法的模型版本，请检查！!")
        if "prediction_corpus_root_path" not in params.keys() or params[
            "prediction_corpus_root_path"] == "None" or params[
            "prediction_corpus_root_path"] is None:
            raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="预测模式下必须输入合法的语料根路径，请检查！!")

        if "prediction_corpus_name" not in params.keys() or params[
            "prediction_corpus_name"] == "None" or params[
            "prediction_corpus_name"] is None:
            raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="预测模式下必须输入合法的语料名称，请检查！!")

        if "prediction_output_path" not in params.keys() or params[
            "prediction_output_path"] == "None" or params[
            "prediction_output_path"] is None:
            raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="预测模式下必须输入合法的结果输出根路径，请检查！!")
        if "prediction_output_name" not in params.keys() or params[
            "prediction_output_name"] == "None" or params[
            "prediction_output_name"] is None:
            raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="预测模式下必须输入合法的结果输出文件名，请检查！!")

    if "use_gpu" not in params.keys() or params["use_gpu"] not in ["true", "false"]:
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="输入参数必须指定GPU模式!")


def check_train_params(train_params):
    try:
        train_params = json.loads(train_params)
    except Exception as e:
        raise KGAlgoException(code=MessageCode.ParamError.second_param_error, message="解析训练配置参数错误，请检查训练参数是否为正确的json格式!",
                              data=str(e))

    if "epochs" not in train_params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.second_param_error,
                              message="解析训练配置参数错误，请确保迭代次数参数存在，并且值为整数字符串!")

    if "incremental_training" not in train_params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.second_param_error, message="解析训练配置参数错误，请确保模型增量标志存在，并且值为布尔值!")


def check_train_stop_params(params):
    if "training_model_name" not in params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="解析停止训练参数错误，请确保模型名称参数存在!")

    if "training_model_version" not in params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="解析停止训练参数错误，请确保模型版本参数存在!")


def check_train_status_params(params):
    if "training_model_root_path" not in params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="解析获取模型状态信息参数错误，请确保模型根路径参数存在!")
    if "training_model_name" not in params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="解析获取模型状态信息参数错误，请确保模型名称参数存在!")

    if "training_model_version" not in params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="解析获取模型状态信息参数错误，请确保模型版本参数存在!")


def check_train_logs_params(params):
    if "training_model_root_path" not in params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="解析获取模型日志信息参数错误，请确保模型根路径参数存在!")
    if "training_model_name" not in params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="解析获取模型日志信息参数错误，请确保模型名称参数存在!")

    if "training_model_version" not in params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="解析获取模型日志信息参数错误，请确保模型版本参数存在!")


def check_predict_stop_params(params):
    if "prediction_model_name" not in params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="解析停止训练参数错误，请确保模型名称参数存在!")

    if "prediction_model_version" not in params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="解析停止训练参数错误，请确保模型版本参数存在!")


def check_predict_status_params(params):
    if "prediction_output_path" not in params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="解析获取预测状态信息参数错误，请确保模型根路径参数存在!")
    if "prediction_output_name" not in params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="解析获取预测状态信息参数错误，请确保模型名称参数存在!")


def check_predict_logs_params(params):
    if "prediction_output_path" not in params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="解析获取预测日志信息参数错误，请确保模型根路径参数存在!")
    if "prediction_output_name" not in params.keys():
        raise KGAlgoException(code=MessageCode.ParamError.first_param_error, message="解析获取预测日志信息参数错误，请确保模型名称参数存在!")
