# -*- coding:utf-8 -*-
import json
import traceback

from flask import Flask, request

from algorithm.communities import personal_communities
from algorithm.degree_centrality import degree_centrality
from algorithm.neighbor_centrality import common_neighbor_centrality
from algorithm.pagerank import personal_pagerank
from algorithm.path_algos import shortest_path, simple_path, graph_traversal
from algorithm.type_probability_graph import type_probability_graph
from tools import error
from tools.error import MessageCode
from tools.param import parser

args = parser.parse_args()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
all_task = {}


@app.route('/kg/compute/algo/pagerank', methods=['POST'])
def kg_compute_algo_pagerank():
    try:
        try:
            data = request.get_json()
        except Exception as e:
            raise error.ParamError("解析参数异常，请检查是否为合格的json字符传格式.")

        try:
            kg_name = data["kg_name"]
            space_name = data["space_name"]
            alpha = data["alpha"]
            max_iter = data["max_iter"]
            topk = data["topk"]
            param = data
            pr_info, statistics_info = personal_pagerank(kg_name, space_name, alpha, max_iter, topk, param)
            result = {"code": MessageCode.NormalCode.normal, "message": "计算 pagerank 成功！",
                      "data": {"nodes": pr_info, "statistics_info": statistics_info}}
            json_result = json.dumps(result, ensure_ascii=False)
            return json_result
        except Exception as e:
            raise error.ComputeError("图计算异常.")
    except Exception as e:
        traceback.print_exc()
        exception_traceback = traceback.format_exc()
        return {"code": MessageCode.AlgoSystemErrorCode.error_code,
                "message": "计算 pagerank 错误，错误详细信息：%s" % exception_traceback, "data": None}


@app.route('/kg/compute/algo/correlation', methods=['POST'])
def kg_compute_algo_correlation():
    try:
        try:
            data = request.get_json()
        except Exception as e:
            raise error.ParamError("解析参数异常，请检查是否为合格的json字符传格式.")

        try:
            kg_name = data["kg_name"]
            space_name = data["space_name"]
            alpha = data["alpha"]
            node = data["node"]
            topk = data["topk"]
            param = data
            correlation, statistics_info = common_neighbor_centrality(kg_name, space_name, node, alpha, topk, param)
            result = {"code": MessageCode.NormalCode.normal, "message": "计算相关性成功！",
                      "data": {"correlation_result": correlation, "statistics_info": statistics_info}}
            json_result = json.dumps(result, ensure_ascii=False)
            return json_result
        except Exception as e:
            raise error.ComputeError("图计算异常.")
    except Exception as e:
        traceback.print_exc()
        exception_traceback = traceback.format_exc()
        return {"code": MessageCode.AlgoSystemErrorCode.error_code,
                "message": "计算 pagerank 错误，错误详细信息：%s" % exception_traceback, "data": None}


@app.route('/kg/compute/algo/communities', methods=['POST'])
def kg_compute_algo_communities():
    try:
        try:
            data = request.get_json()
        except Exception as e:
            raise error.ParamError("解析参数异常，请检查是否为合格的json字符传格式.")

        try:
            kg_name = data["kg_name"]
            space_name = data["space_name"]
            weight = None if "weight" not in data else data["weight"]
            resolution = 1 if "resolution" not in data else data["resolution"]
            cutoff = 1 if "cutoff" not in data else data["cutoff"]
            best_n = None if "best_n" not in data else data["best_n"]
            param = data
            info, statistics_info = personal_communities(kg_name, space_name, param, weight, resolution, cutoff, best_n)
            result = {"code": MessageCode.NormalCode.normal, "message": "计算 communities 成功！",
                      "data": {"nodes": info, "statistics_info": statistics_info}}
            json_result = json.dumps(result, ensure_ascii=False)
            return json_result
        except Exception as e:
            raise error.ComputeError("图计算异常.")
    except Exception as e:

        traceback.print_exc()
        exception_traceback = traceback.format_exc()
        return {"code": MessageCode.AlgoSystemErrorCode.error_code,
                "message": "计算 pagerank 错误，错误详细信息：%s" % exception_traceback, "data": None}


@app.route('/kg/compute/algo/shortest_path', methods=['POST'])
def kg_compute_algo_shortest_path():
    try:
        try:
            data = request.get_json()
        except Exception as e:
            raise error.ParamError("解析参数异常，请检查是否为合格的json字符传格式.")

        try:
            kg_name = data["kg_name"]
            space_name = data["space_name"]
            param = data
            source = None if "source" not in data else data["source"]
            target = None if "target" not in data else data["target"]
            method = "max" if "method" not in data else data["method"]  # method = "max","min"
            filter_event = False if "filter_event" not in data else data["filter_event"]
            info = shortest_path(kg_name, space_name, param, source, target, method, filter_event)
            result = {"code": MessageCode.NormalCode.normal, "message": "计算 shortest_path 成功！", "data": {"edges": info}}
            json_result = json.dumps(result, ensure_ascii=False)
            return json_result
        except Exception as e:
            raise error.ComputeError("图计算异常.")
    except Exception as e:

        traceback.print_exc()
        exception_traceback = traceback.format_exc()
        return {"code": MessageCode.AlgoSystemErrorCode.error_code,
                "message": "计算 pagerank 错误，错误详细信息：%s" % exception_traceback, "data": None}


@app.route('/kg/compute/algo/simple_path', methods=['POST'])
def kg_compute_algo_simple_path():
    try:
        try:
            data = request.get_json()
        except Exception as e:
            raise error.ParamError("解析参数异常，请检查是否为合格的json字符传格式.")

        try:
            kg_name = data["kg_name"]
            space_name = data["space_name"]
            source = data["source"]
            target = data["target"]
            filter_event = False if "filter_event" not in data else data["filter_event"]
            info = simple_path(kg_name, space_name, source, target, filter_event)
            result = {"code": MessageCode.NormalCode.normal, "message": "计算 simple_path 成功！", "data": {"edges": info}}
            json_result = json.dumps(result, ensure_ascii=False)
            return json_result
        except Exception as e:
            raise error.ComputeError("图计算异常.")
    except Exception as e:

        traceback.print_exc()
        exception_traceback = traceback.format_exc()
        return {"code": MessageCode.AlgoSystemErrorCode.error_code,
                "message": "计算 pagerank 错误，错误详细信息：%s" % exception_traceback, "data": None}


@app.route('/kg/compute/algo/traversal', methods=['POST'])
def kg_compute_algo_traversal():
    try:
        try:
            data = request.get_json()
        except Exception as e:
            raise error.ParamError("解析参数异常，请检查是否为合格的json字符传格式.")

        try:
            kg_name = data["kg_name"]
            space_name = data["space_name"]
            param = data
            source = data["source"]
            depth_limit = None if "depth_limit" not in data else data["depth_limit"]
            method = "dfs" if "method" not in data else data["method"]
            info = graph_traversal(kg_name, space_name, param, source, depth_limit, method)
            result = {"code": MessageCode.NormalCode.normal, "message": "计算 traversal 成功！", "data": {"nodes": info}}
            json_result = json.dumps(result, ensure_ascii=False)
            return json_result
        except Exception as e:
            raise error.ComputeError("图计算异常.")
    except Exception as e:

        traceback.print_exc()
        exception_traceback = traceback.format_exc()
        return {"code": MessageCode.AlgoSystemErrorCode.error_code,
                "message": "计算 pagerank 错误，错误详细信息：%s" % exception_traceback, "data": None}


@app.route('/kg/compute/algo/pot', methods=['POST'])
def kg_compute_algo_type_probability_graph():
    try:
        try:
            data = request.get_json()
        except Exception as e:
            raise error.ParamError("解析参数异常，请检查是否为合格的json字符传格式.")

        try:
            kg_name = data["kg_name"]
            space_name = data["space_name"]
            type_filter = data["type_filter"]
            param = data
            probability, statistics_info = type_probability_graph(kg_name, space_name, type_filter, param)
            result = {"code": MessageCode.NormalCode.normal, "message": "计算节点类型概率图成功！",
                      "data": {"probability": probability, "statistics_info": statistics_info}}
            json_result = json.dumps(result, ensure_ascii=False)
            return json_result
        except Exception as e:
            raise error.ComputeError("图计算异常.")
    except Exception as e:

        traceback.print_exc()
        exception_traceback = traceback.format_exc()
        return {"code": MessageCode.AlgoSystemErrorCode.error_code,
                "message": "计算 pagerank 错误，错误详细信息：%s" % exception_traceback, "data": None}


@app.route('/kg/compute/algo/degreecentrality', methods=['POST'])
def kg_compute_algo_degree_centrality():
    try:
        try:
            data = request.get_json()
        except Exception as e:
            raise error.ParamError("解析参数异常，请检查是否为合格的json字符传格式.")

        try:
            kg_name = data["kg_name"]
            space_name = data["space_name"]
            topk = data["topk"]
            param = data
            degree, statistics_info = degree_centrality(kg_name, space_name, topk, param)
            result = {"code": MessageCode.NormalCode.normal, "message": "计算度中心性成功！",
                      "data": {"degree_centrality": degree, "statistics_info": statistics_info}}
            json_result = json.dumps(result, ensure_ascii=False)
            return json_result
        except Exception as e:
            raise error.ComputeError("图计算异常.")
    except Exception as e:

        traceback.print_exc()
        exception_traceback = traceback.format_exc()
        return {"code": MessageCode.AlgoSystemErrorCode.error_code,
                "message": "计算 pagerank 错误，错误详细信息：%s" % exception_traceback, "data": None}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
