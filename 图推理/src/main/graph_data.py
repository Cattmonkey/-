# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
import json

import networkx as nx
import numpy as np
from nebula3.Config import Config
from nebula3.gclient.net import ConnectionPool

from config import KG_SOURCE_CONFIG
from tools import error
from tools.math import MathTools

GRAPH = {}

DEFAULT_WEIGHT = 0.1
FLOAT_PRECESSION = 5

"""
1）从图数据库中读取数据;
2）根据图数据库中的节点属性与关系属性构造图数据;
3）根据具体的计算任务生成相应的个性化图数据.

读取后节点与边的存储方式：
# 节点读取后的存储方式：
nodes = {"node_id":{
    "node_id": "xxx",  # 节点的ID，如644687315412315
    "name": "xxx",  # 节点的名称，如“华盛顿号航空母舰”
    "node_type": "xxx",  # 节点的类型，如航空母舰
    "node_type_id": "xxx",  # 节点类型的ID,如航空母舰的ID,12465431566
    "attributes":  # 节点的所有属性，参与节点的权重计算
        {
            "att1": "xxx",  # 如排水量->10
            "att2": "xxx",  # 如满载人数->300
            "attk": "xxx"

        }}}
        
# 边读取后的存储方式：
edges = {"edge_id":{
    "edge_id": "xxx",  # 边的ID,如：16764641231342
    "name": "xxx",  # 边的名称，如：驶入
    "start_entity": "xxx",  # 关系头实体ID,如：444611243121234315
    "end_entity": "xxx",  # 关系头实体ID，如：8512423312122
    "edge_type_id": "xxx",  # 边的类型ID，如驶入的ID，44242244222
    "attributes": {  # 边的属性，参与节点的权重计算
        "att1": "xxx",  # 如日期，时间戳65412512251
        "att2": "xxx",
        "attk": "xxx"
    }}}
"""


# 数据读取的接口及参数
def read_graph_data(space_name, kg_name, graph_rules, direction, edge_function, filter_event=False, filter_node_ids=[],
                    filter_relation_ids=[]):
    """
    1）该函数从图数据库中读取数据，返回一个基于network的有向或无向图；
    2）并根节点与边的属性权重配置生成节点和边的权重；
    3）根据算法需要构建有向图或无向图；
    4）根据具体算法特性对多条边的权重进行处理

    :param space_name: # 数据库空间，用于读取数据
    :param kg_name: # 数据名称，用于读取数据
    :param graph_rules: # 权重配置参数
    :param direction: # 所构造图的方向
    :param edge_function: # 边处理函数名称
    :return: network图数据对象
    """
    # 参数校验，本部分参数校验只对 graph_rules 进行校验
    print("======================================== 图数据库读取规则配置参数： ========================================")
    print(graph_rules)

    try:
        # 参数校验
        graph_rules_check(graph_rules)
        # 定义图数据库链接配置
        config = Config()
        config.max_connection_pool_size = 10
        # 初始化连接池
        connection_pool = ConnectionPool()
        # 如果给定的服务器正常，则返回true，否则返回false。

        try:
            ok = connection_pool.init([(KG_SOURCE_CONFIG["ip"], KG_SOURCE_CONFIG["port"])], config)
            # 从连接池中获取会话
            session = connection_pool.get_session(KG_SOURCE_CONFIG["user"], KG_SOURCE_CONFIG["password"])
        except Exception as e:
            print(e)
            raise error.GetDataError("图数据库链接异常异常.")
        # 选择图空间
        session.execute('USE `%s`' % space_name)
        # 执行查看TAG命令
        tags = session.execute('SHOW TAGS')
        if tags.is_empty():
            raise error.GetDataError("读取节点数据为空.详细信息:%s" % str(tags))
        print("======================================== SHOW TAGS： ========================================")
        print(tags)
        """
        解析节点数据
        # """
        nodes_data = {}
        for tag in tags:
            tag = str(tag).replace("\"", "")
            nodes_sql = "MATCH (v:`%s`{graphId:'%s'}) return v" % (tag, kg_name)
            try:
                kg_nodes_data = json.loads(session.execute_json(nodes_sql))
                if len(kg_nodes_data["results"][0]["data"]) == 0:
                    raise error.GetDataError("没有读取到节点数据，请检查图数据库信息配置是否正确.")
            except Exception as e:
                raise error.GetDataError("读取图数据节点异常.")
            try:
                if kg_nodes_data["errors"][0]["code"] == 0:
                    rows = kg_nodes_data["results"][0]['data']
                    for r in rows:
                        attributes = r["row"][0]
                        node_type_id = list(attributes.keys())[0].split(".")[0]
                        node_id = r["meta"][0]["id"]
                        if node_id in filter_node_ids:
                            continue
                        new_attributes, name, vertex_type = convert_attribute(attributes)
                        nodes_data[node_id] = {"name": name,
                                               "node_type": vertex_type,
                                               "node_type_id": node_type_id,
                                               "attributes": new_attributes}
                else:
                    raise error.GetDataError("读取节点错误；%s" % str(kg_nodes_data))

            except Exception as e:
                raise error.DataPreProcessError("解析图数据节点异常；%s" % str(e))

        print("解析完节点信息后的节点数据量:%s", str(len(nodes_data)))
        edges_id = session.execute('SHOW EDGES')
        if edges_id.is_empty():
            raise error.GetDataError("读取边数据为空.详细信息:%s" % str(edges_id))

        print("======================================== SHOW EDGES： ========================================")
        print(edges_id)

        """
        解析边数据
        """
        edges_data = {}
        for i in range(len(edges_id.rows())):
            e_id = str(edges_id.row_values(i)[0]).replace("\"", "")
            sql = "MATCH p=(v1)-[e:`%s`{graphId:'%s'}]-(v2) return p" % (e_id, kg_name)
            try:
                spo = json.loads(session.execute_json(sql))
                if len(spo["results"][0]["data"]) == 0:
                    raise error.GetDataError("没有读取到边数据，请检查图数据库信息配置是否正确.")
                if spo["errors"][0]["code"] == 0:
                    rows = spo["results"][0]['data']

                    for r in rows:
                        # todo 加入边带上来的新节点
                        # 获取边的第一个实体
                        entity_1_id = r["meta"][0][0]["id"]
                        entity_1_attributes = r["row"][0][0]
                        entity_1_type_id = list(entity_1_attributes.keys())[0].split(".")[0]
                        entity_1_new_attributes, entity_1_name, entity_1_vertex_type = convert_attribute(
                            entity_1_attributes)
                        if entity_1_id not in nodes_data.keys():
                            nodes_data[entity_1_id] = {"name": entity_1_name,
                                                       "node_type": entity_1_vertex_type,
                                                       "node_type_id": entity_1_type_id,
                                                       "attributes": entity_1_new_attributes}
                        # 获取边的第一个实体
                        entity_2_id = r["meta"][0][2]["id"]
                        entity_2_attributes = r["row"][0][2]
                        entity_2_type_id = list(entity_2_attributes.keys())[0].split(".")[0]
                        entity_2_new_attributes, entity_2_name, entity_2_vertex_type = convert_attribute(
                            entity_2_attributes)
                        if entity_2_id not in nodes_data.keys():
                            nodes_data[entity_2_id] = {"name": entity_2_name,
                                                       "node_type": entity_2_vertex_type,
                                                       "node_type_id": entity_2_type_id,
                                                       "attributes": entity_2_new_attributes}

                        if filter_event and r['row'][0][1]['edgeType'] == 'EVENT':
                            continue
                        if r["meta"][0][1]["id"]["dst"] in filter_node_ids or r["meta"][0][1]["id"][
                            "src"] in filter_node_ids:
                            continue
                        if r["meta"][0][1]["id"] in filter_relation_ids:
                            continue
                        edge = {"edge_type_id": r["meta"][0][1]["id"]["name"]}
                        if r["meta"][0][1]["id"]["type"] > 0:
                            edge["end_entity"] = r["meta"][0][1]["id"]["dst"]
                            edge["start_entity"] = r["meta"][0][1]["id"]["src"]
                        else:
                            edge["end_entity"] = r["meta"][0][1]["id"]["src"]
                            edge["start_entity"] = r["meta"][0][1]["id"]["dst"]
                        edge["name"] = r["row"][0][1]["name"]
                        row = r["row"][0]
                        edge["attributes"] = {}
                        for re in row[1].keys():
                            if re not in ["name", "edgeId", "graphId"]:
                                edge["attributes"][re] = row[1][re]
                        edges_data[row[1]["edgeId"]] = edge
                else:
                    raise error.GetDataError("读取边错误；%s" % str(spo))
            except Exception as e:
                raise e
        print("解析完边信息后的节点数据量:%s", str(len(nodes_data)))

        # 释放会话
        session.release()
        # 关闭连接池
        connection_pool.close()
        print("======================================== 数据读取完成，数据预处理开始： ========================================")

        # 统计数值化属性的数据分布,根据规则配置，将规则中标明是数值属性的数据抽取数来，以便后续处理
        statistic_attribute = statistic_numerical_attributes(nodes_data, edges_data,
                                                             graph_rules["attributes"])
        # 图初始化
        if direction:
            G = nx.DiGraph()
        else:
            G = nx.Graph()
        for k in nodes_data.keys():
            G.add_node(k, weights=DEFAULT_WEIGHT)
        for e in edges_data.keys():
            G.add_edge(edges_data[e]["start_entity"], edges_data[e]["end_entity"], weights=DEFAULT_WEIGHT)

        print("======================================== nodes_data: ========================================")
        print(nodes_data)

        # 为节点计算权重,多进程计算
        nodes_weight = nodes_weight_multiprocessing(nodes_data=nodes_data, graph_rules=graph_rules,
                                                    statistic_attribute=statistic_attribute,
                                                    edge_function=edge_function)
        for k in nodes_weight:
            w = round(float(nodes_weight[k]), FLOAT_PRECESSION)
            G.nodes()[k]['weights'] = w
        print("======================================== 节点及其权重: ========================================")
        for n in G.nodes(data=True):
            print(n, nodes_data[n[0]]["name"])

        print("======================================== edges_data: ========================================")
        print(edges_data)

        # 为边计算权重,多进程计算
        edges_weight, all_edges = edges_weight_multiprocessing(edges_data=edges_data, graph_rules=graph_rules,
                                                               statistic_attribute=statistic_attribute,
                                                               edge_function=edge_function)
        for k in edges_weight:
            w = edges_weight[k]["weight"]
            # todo 处理两点多边问题

            G.add_edge(edges_weight[k]["start_entity"], edges_weight[k]["end_entity"], weights=w)
        print("======================================== 边及其权重 ========================================")
        for _ in G.edges(data=True):
            print(_, nodes_data[_[0]]["name"], nodes_data[_[1]]["name"])
        return_data = [G, nodes_data, edges_data, all_edges]
        return return_data
    except Exception as e:
        raise e


def data_split(data, parts):
    if parts > len(data):
        return [data]

    def EveryStrandIsN(listTemp, n):
        for i in range(0, len(listTemp), n):
            yield listTemp[i:i + n]

    parts = len(data) // parts
    keys_list = EveryStrandIsN(list(data.keys()), parts)

    result = []
    for a_list in keys_list:
        temp = {}
        for i in a_list:
            temp[i] = data[i]
        result.append(temp)

    return result


def node_weights_evaluation(data, graph_rules, statistic_attribute, edge_function):
    result = {}
    for k in data.keys():
        if len(data[k]["attributes"]) < 0:
            w = 0.0
        else:
            weights = dict(zip(data[k]["attributes"].keys(), [DEFAULT_WEIGHT] * len(data[k]["attributes"].keys())))
            for rule in graph_rules["attributes"]:
                for att in data[k]["attributes"]:
                    if att == rule["attribute_id"] and data[k]["node_type_id"] == rule["type_id"]:
                        value = attributes_condition(data[k], rule, statistic_attribute)  #
                        if value:
                            weights[att] = value
            w = cal_attribute_weight(weights, function_name=edge_function)
        result[k] = round(w, FLOAT_PRECESSION)
    return result


def calc_multi_edges(all_edges, method='avg'):
    result = dict()
    for key in all_edges.keys():
        start_entity, end_entity = key.split(',')
        arr = []
        for i in all_edges[key]:
            for j in i.values():
                arr.append(j)
        if method == 'avg':
            weight = np.array(arr).mean()
        elif method == 'max':
            weight = np.array(arr).max()
        elif method == 'min':
            weight = np.array(arr).min()
        result[key] = {"start_entity": start_entity,
                       "end_entity": end_entity,
                       "weight": weight}
    return result


def edge_weights_evaluation(data, graph_rules, statistic_attribute, edge_function):
    all_edges = dict()
    result = {}
    for k in data.keys():
        if len(data[k]["attributes"]) < 0:
            w = 0.0
        else:
            weights = dict(zip(data[k]["attributes"].keys(), [DEFAULT_WEIGHT] * len(data[k]["attributes"].keys())))
            for rule in graph_rules["attributes"]:
                # 规则分类
                for att in data[k]["attributes"].keys():
                    if att == rule["attribute_id"] and data[k]["edge_type_id"] == rule["type_id"]:
                        # print(ed[k]["attributes"]["type_id"], ": 边属性：", att)
                        value = attributes_condition(data[k], rule, statistic_attribute)  # 规则
                        if value:
                            weights[att] = value
                        # print("计算权重后的weights:", weights)

            # 边直接赋值
            w = cal_attribute_weight(weights, function_name=edge_function)  # weight建模
            for rule in graph_rules["relations"]:
                if data[k]["edge_type_id"] == rule["relation_id"]:
                    w = rule['weight_subject_to'][0]
            w = round(w, FLOAT_PRECESSION)
        key = data[k]["start_entity"] + "," + data[k]["end_entity"]
        if key in all_edges:
            temp = all_edges[key]
            temp.append({k: w})
            all_edges[key] = temp
        else:
            all_edges[key] = [{k: w}]
        # result[k] = {"start_entity": data[k]["start_entity"],
        #              "end_entity": data[k]["end_entity"],
        #              "weight": w
        #              }
    return all_edges


def nodes_weight_multiprocessing(nodes_data, graph_rules, statistic_attribute, edge_function):
    # 直接运行，非多进程
    result = node_weights_evaluation(nodes_data, graph_rules, statistic_attribute, edge_function)

    # 设置进程数
    # 根据 process_num 平均切分 nodes_data
    # process_num = 4
    # nodes_data_split = data_split(nodes_data, process_num)
    # 多进程运行
    # pool = Pool(processes=process_num)
    # result_list = []
    # for nodes in nodes_data_split:
    #     result_list.append(pool.apply_async(node_weights_evaluation, (
    #         nodes, params, statistic_attribute, edge_function,)))
    # pool.close()
    # pool.join()
    # result = {}
    # for i in result_list:
    #     i_result = i.get()
    #     result.update(i_result)
    # 以上多进程运行

    return result


def edges_weight_multiprocessing(edges_data, graph_rules, statistic_attribute, edge_function):
    # 直接运行，非多进程
    result = edge_weights_evaluation(edges_data, graph_rules, statistic_attribute, edge_function)
    r = calc_multi_edges(result)
    # 根据 process_num 平均切分 nodes_data
    # process_num = 4
    # nodes_data_split = data_split(edges_data, process_num)
    # 多进程运行
    # pool = Pool(processes=process_num)
    # result_list = []
    # for edges in nodes_data_split:
    #     result_list.append(pool.apply_async(edge_weights_evaluation, (
    #         edges, params, statistic_attribute, edge_function,)))
    # pool.close()
    # pool.join()
    # result = {}
    # for i in result_list:
    #     i_result = i.get()
    #     result.update(i_result)
    # 以上多进程运行

    return r, result


def convert_attribute(d):
    """
    将图数据中读取的节点描述信息和属性信息分离出来
    :param d:
    :return:
    """
    r = {}
    name = None
    vertex_type = None
    for key in d.keys():
        if "graphId" not in key and 'vertexType' not in key and "name" not in key:
            value = d[key]
            key = key.split(".")[1]
            r[key] = value
        if "name" in key:
            name = d[key]
        if "vertexType" in key:
            vertex_type = d[key]
    return r, name, vertex_type


def statistic_numerical_attributes(nodes_data, edges_data, rules):
    """
    根据规则配置，将规则中标明是数值属性的数据抽取数来，以便后续处理
    :param nodes_data:
    :param edges_data:
    :param rules:
    :return:
    """
    statistic_attribute = {}
    # 复杂度m*n
    for rule in rules:
        if rule["value_type"] == "NUMERICAL":
            value_list = []
            # 统计节点的数值属性
            for k in nodes_data.keys():
                if rule["attribute_id"] in nodes_data[k]["attributes"].keys():
                    if not nodes_data[k]["attributes"][rule["attribute_id"]]:
                        continue
                    value_list.append(float(nodes_data[k]["attributes"][rule["attribute_id"]]))

            # 统计边的数值属性
            for k in edges_data.keys():
                if rule["attribute_id"] in edges_data[k]["attributes"].keys():
                    if not edges_data[k]["attributes"][rule["attribute_id"]]:
                        continue
                    value_list.append(float(edges_data[k]["attributes"][rule["attribute_id"]]))
            statistic_attribute[rule["attribute_id"]] = value_list
        return statistic_attribute


def cal_attribute_weight(weights, alpha=0.95, beta=1, function_name=None):
    print("cal_attribute_weight")
    print(weights)

    if len(weights) == 0:
        return DEFAULT_WEIGHT

    # result = 0
    # for w in weights:
    #     if abs(weights[w] - 0.1) < 1e-5:
    #         result += weights[w]
    #     else:
    #         result += (weights[w] * (1+alpha)) ** beta
    # result /= len(weights)
    def func_calc(args):
        return 0

    if function_name == "avg":
        result = np.mean(list(weights.values()))
    elif function_name == "max":
        result = np.max(list(weights.values()))
    elif function_name == "min":
        result = np.min(list(weights.values()))
    elif function_name == "xxx":
        result = func_calc(list(weights.values()))
    else:
        return DEFAULT_WEIGHT
    return result


def attributes_condition(data_object, condition_dict, statistic_attribute):
    """

    :param data_object:
    :param condition_dict:
    :param statistic_attribute:
    :return:
    """
    if condition_dict['type'] in ['ENTITY', "EVENT", "RELATION"]:
        rule_value_type = condition_dict["value_type"]  # 属性数据类型，数值型或字符型
        rule_operator = condition_dict["rule"]  # 属性运算符
        rule_attribute_id = condition_dict["attribute_id"]  # 规则中所指定的参与运算的属性
        data_attribute_value = data_object["attributes"][condition_dict["attribute_id"]]  # 输入数据中所要参与运算的属性值
        rule_subject_to = condition_dict["rule_subject_to"]
        weight_subject_to = condition_dict['weight_subject_to']

        if rule_value_type == "CHARACTER":
            if rule_operator == "EQ":
                if data_attribute_value == rule_subject_to[0]:
                    if len(weight_subject_to) == 0:
                        raise error.ParamError("规则%s的\"weight_subject_to\"需要一个在[0,1]区间的数！" % str(condition_dict))
                    return weight_subject_to[0]
            elif rule_operator == "CONTAINS":
                if data_attribute_value and rule_subject_to[0] in data_attribute_value:
                    if len(weight_subject_to) == 0:
                        raise error.ParamError("规则%s的\"weight_subject_to\"需要一个在[0,1]区间的数！" % str(condition_dict))
                    return weight_subject_to[0]
            elif rule_operator in ["ASCENDING", "DESCENDING"]:
                if not len(weight_subject_to) == 2:
                    raise error.ParamError("规则%s的\"weight_subject_to\"需要指定一个[0,1]子的区间！" % str(condition_dict))
                [_min, _max] = weight_subject_to
                _min = 0.1 if MathTools.equal_or_smaller_than(_min, 0.1) else _min
                length = len(rule_subject_to)
                if length <= 1:
                    return DEFAULT_WEIGHT
                inter = (_max - _min) / (length - 1)
                new_condition = []
                for i in range(length):
                    new_condition.append(_min + i * inter)
                if rule_operator == "ASCENDING":
                    return new_condition[rule_subject_to.index(data_attribute_value)]
                else:
                    a = rule_subject_to.index(data_attribute_value)
                    return new_condition[length - 1 - rule_subject_to.index(
                        data_object[condition_dict["attribute_id"]])]

        if rule_value_type == "NUMERICAL":
            rule_subject_to = [float(_) for _ in rule_subject_to]
            if not data_attribute_value:
                return None
            if rule_operator == "BETWEEN":
                if MathTools.is_in_region(float(data_attribute_value), rule_subject_to[0], rule_subject_to[1]):
                    if len(weight_subject_to) == 0:
                        raise error.ParamError("规则%s的\"weight_subject_to\"需要一个在[0,1]区间的数！" % str(condition_dict))
                    return weight_subject_to[0]
            elif rule_operator == "GT":
                if MathTools.bigger_than(float(data_attribute_value), rule_subject_to[0]):
                    if len(weight_subject_to) == 0:
                        raise error.ParamError("规则%s的\"weight_subject_to\"需要一个在[0,1]区间的数！" % str(condition_dict))
                    return weight_subject_to[0]
            elif rule_operator == "LT":
                if MathTools.smaller_than(float(data_attribute_value), rule_subject_to[0]):
                    if len(weight_subject_to) == 0:
                        raise error.ParamError("规则%s的\"weight_subject_to\"需要一个在[0,1]区间的数！" % str(condition_dict))
                    return weight_subject_to[0]
            elif rule_operator == "GEQ":
                if MathTools.equals_or_bigger_than(float(data_attribute_value), rule_subject_to[0]):
                    if len(weight_subject_to) == 0:
                        raise error.ParamError("规则%s的\"weight_subject_to\"需要一个在[0,1]区间的数！" % str(condition_dict))
                    return weight_subject_to[0]
            elif rule_operator == "LEQ":
                if MathTools.equal_or_smaller_than(float(data_attribute_value), rule_subject_to[0]):
                    if len(weight_subject_to) == 0:
                        raise error.ParamError("规则%s的\"weight_subject_to\"需要一个在[0,1]区间的数！% str(condition_dict)")
                    return weight_subject_to[0]
            elif rule_operator == "EQ":
                if MathTools.is_equal(float(data_attribute_value), rule_subject_to[0]):
                    if len(weight_subject_to) == 0:
                        raise error.ParamError("规则%s的\"weight_subject_to\"需要一个在[0,1]区间的数！" % str(condition_dict))
                    return weight_subject_to[0]
            elif rule_operator in ["DESCENDING", "ASCENDING"]:
                if not len(weight_subject_to) == 2:
                    raise error.ParamError("规则%s的\"weight_subject_to\"需要指定一个[0,1]子的区间！" % str(condition_dict))
                sort_list = statistic_attribute[condition_dict["attribute_id"]]
                sort_list.sort()
                sort_list = np.array(sort_list)
                mean = sort_list.mean()
                std = sort_list.std()
                if MathTools.is_equal(std, 0.0):
                    return 0.5
                sort_list = (sort_list - mean) / std
                temp = (float(data_attribute_value) - mean) / std
                if MathTools.is_equal(max(sort_list), min(sort_list)):
                    return DEFAULT_WEIGHT
                r = (temp - min(sort_list)) / (max(sort_list) - min(sort_list)) * (
                        weight_subject_to[1] - weight_subject_to[0])
                r = round(r, FLOAT_PRECESSION)
                if MathTools.bigger_than(r, 1.0) or MathTools.smaller_than(r, 0):
                    print("z-score problem!!!", r)
                if rule_operator == "DESCENDING":
                    if MathTools.is_equal(1.0, r):
                        r = 0.9
                    return 1.0 - r
                else:
                    if MathTools.is_equal(1, 0.0):
                        r = DEFAULT_WEIGHT
                    return r
    return None


def graph_rules_check(graph_rules):
    """
    对于构建图的规则参数进行校验
    :param graph_rules: 字典形式参数，
    :return:
    """
    # 第一层校验
    if not type(graph_rules) == type(dict()):
        raise error.ParamError("图构建规则参数不是一个json对象，请查看输入参数的\"graph_rules\"字段！")
    # todo 保留
    # if not set(["entities", "relations", "attributes"]) == set(list(graph_rules.keys())):
    #     raise KGAlgoException(code=MessageCode.ParamError.type_error,
    #                           message="请确保规则参数存在\"entities\",\"relations\",\"attributes\"字段信息！")
    # todo 实体直接赋权重校验
    # 预留

    # 关系直接赋权重校验
    for relation_rule in graph_rules["relations"]:
        if not set(["type", "relation_id", "start_type_id", "end_type_id", "weight_subject_to"]) == set(
                list(relation_rule.keys())):
            raise error.ParamError("请确保规则%s存在\"type\", \"relation_id\", \"start_type_id\", \"end_type_id\","
                                   " \"weight_subject_to\"字段信息！" % str(relation_rule))

        if len(relation_rule["weight_subject_to"]) == 0:
            raise error.ParamError("请确保规则%s的\"weight_subject_to\"字段内容不为空！" % str(relation_rule))

        if not MathTools.is_in_region(value=relation_rule["weight_subject_to"][0], lower_bound=0.0, upper_bound=1.0):
            raise error.ParamError("请确保规则%s的\"weight_subject_to\"字段内容在[0,1]区间内！" % str(relation_rule))

    # 属性（实体属性于关系属性）赋权重校验
    for attribute_rule in graph_rules["attributes"]:

        key_set = set(["type", "type_id", "attribute_id", "value_type", "rule", "rule_subject_to", "weight_subject_to"])
        if not key_set == set(list(attribute_rule.keys())):
            raise error.ParamError("请确保规则%s存在\"type\",\"type_id\",\"attribute_id\",\"value_type\","
                                   "\"rule\",\"rule_subject_to\",\"weight_subject_to\"字段信息！" % str(
                attribute_rule))
        # if len(attribute_rule["rule_subject_to"]) == 0:
        #     raise KGAlgoException(code=MessageCode.ParamError.type_error,
        #                           message="请确保规则%s的\"rule_subject_to\"字段内容不为空！" % str(attribute_rule))

        if len(attribute_rule["weight_subject_to"]) == 0:
            raise error.ParamError("请确保规则%s的\"weight_subject_to\"字段内容不为空！" % str(attribute_rule))

        if not MathTools.is_in_region(value=attribute_rule["weight_subject_to"][0], lower_bound=0.0, upper_bound=1.0):
            raise error.ParamError("请确保规则%s的\"weight_subject_to\"字段内容在[0,1]区间内！" % str(attribute_rule))


if __name__ == '__main__':
    a = {}
    b = type(a)
    pass
