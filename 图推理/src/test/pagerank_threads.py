# -*- coding:utf-8 -*-
import json
from tools.error import KGAlgoException
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from nebula3.Config import Config
from nebula3.gclient.net import ConnectionPool

from config import KG_SOURCE_CONFIG
import threadpool
from multiprocessing import Pool

GRAPH = {}

DEFAULT_WEIGHT = 0.1
FLOAT_PRECESSION = 5

################################################################################
def weights_evaluation(func_type, k, info, param, statistic_attribute, des=None):
    if func_type == "node":
        weights = dict(zip(info.keys(), [0.1] * len(info.keys())))
        for rule in param["graph_rules"]["attributes"]:
            for att in info:
                if att == rule["attribute_id"] and des["node_type_id"] == rule["type_id"]:
                    # print("节点属性：", att)
                    value = attributes_condition(info, rule, statistic_attribute)  #
                    if value:
                        weights[att] = value
                    # print("计算权重后的weights:", weights)
                    # print("计算%s后的临时weights:", cal_weight(weights) %att)
        w = cal_weight(weights)
    else:
        weights = dict(zip(info["attributes"].keys(), [0.1] * len(info["attributes"].keys())))
        for rule in param["graph_rules"]["attributes"]:
            # 规则分类
            for att in info["attributes"].keys():
                if att == rule["attribute_id"] and info["edge_type_id"] == rule["type_id"]:
                    # print(ed[k]["attributes"]["type_id"], ": 边属性：", att)
                    value = attributes_condition(info["attributes"], rule, statistic_attribute)  # 规则
                    if value:
                        weights[att] = value
                    # print("计算权重后的weights:", weights)

        # 边直接赋值

        # print("计算权重后的weights:", weights)
        w = cal_weight(weights)  # weight建模
        for rule in param["graph_rules"]["relations"]:
            if info["edge_type_id"] == rule["relation_id"]:
                w = rule['weight_subject_to'][0]
    w = round(float(w), FLOAT_PRECESSION)
    return {k: w}
##################################################################################

def personal_pagerank(kg_name, space_name, alpha, max_iter, topk, param):
    try:
        print("======================================== 输入参数 ========================================")
        print(param)
        # # 定义配置
        config = Config()
        config.max_connection_pool_size = 10
        # 初始化连接池
        connection_pool = ConnectionPool()
        # 如果给定的服务器正常，则返回true，否则返回false。
        ok = connection_pool.init([(KG_SOURCE_CONFIG["ip"], KG_SOURCE_CONFIG["port"])], config)

        # 方法1：控制连接自行释放。
        # 从连接池中获取会话
        session = connection_pool.get_session(KG_SOURCE_CONFIG["user"], KG_SOURCE_CONFIG["password"])
        # 选择图空间
        session.execute('USE `%s`' % space_name)
        # session.execute('USE %s' % kg_name)

        # 执行查看TAG命令
        tags = session.execute('SHOW TAGS')
        print("======================================== SHOW TAGS ========================================")
        nodes_sql = "MATCH (v) return v LIMIT 10000"
        try:
            kg_nodes_info = json.loads(session.execute_json(nodes_sql))
            # kg_nodes_info = get_nodes()
        except Exception as e:
            print("查询节点数据错误！")
            print(e)
        node_des = {}
        read_nodes = {}
        try:
            if kg_nodes_info["errors"][0]["code"] == 0:
                rows = kg_nodes_info["results"][0]['data']
                for r in rows:
                    attributes = r["row"][0]
                    node_type_id = list(attributes.keys())[0].split(".")[0]
                    node_id = r["meta"][0]["id"]
                    new_attributes, name, vertex_type = convert_attribute(attributes)
                    read_nodes[node_id] = new_attributes
                    node_des[node_id] = {"name": name, "node_type": vertex_type,
                                         "node_type_id": node_type_id}

        except Exception as e:
            print(e)

        edges_id = session.execute('SHOW EDGES')
        ed = {}
        for i in range(len(edges_id.rows())):
            e_id = str(edges_id.row_values(i)[0]).replace("\"", "")
            sql = "MATCH p=(v1)-[e:`%s`]-(v2) return p" % e_id
            try:
                spo = json.loads(session.execute_json(sql))
                # spo = get_triples()
                pass
            except Exception as e:
                print("查询数据错误！")
                print(e)
            try:
                if spo["errors"][0]["code"] == 0:
                    rows = spo["results"][0]['data']
                    for r in rows:
                        e = {}
                        # edge_id = r["meta"][0][1]["id"]["name"]
                        e["edge_type_id"] = r["meta"][0][1]["id"]["name"]
                        if r["meta"][0][1]["id"]["type"] > 0:
                            e["end_entity"] = r["meta"][0][1]["id"]["dst"]
                            e["start_entity"] = r["meta"][0][1]["id"]["src"]
                        else:
                            e["end_entity"] = r["meta"][0][1]["id"]["src"]
                            e["start_entity"] = r["meta"][0][1]["id"]["dst"]
                        row = r["row"][0]
                        e["attributes"] = {}
                        for re in row[1].keys():
                            if re not in ["name", "edgeId", "direction", "graphId", "edgeType"]:
                                e["attributes"][re] = row[1][re]
                        ed[row[1]["edgeId"]] = e
            except Exception as e:
                print(e)
        # 释放会话
        session.release()
        # 关闭连接池
        connection_pool.close()
        """以上是数据库链接"""
        with open(
                "D:\work\project\implementation\HT-kg-platform\kg-compute\\network-x\data\kg_data\\480318500696793088\\nodes.json",
                "w", encoding="utf-8") as f:
            json.dump(read_nodes, f, ensure_ascii=False)

        with open(
                "D:\work\project\implementation\HT-kg-platform\kg-compute\\network-x\data\kg_data\\480318500696793088\\nodes_des.json",
                "w", encoding="utf-8") as f:
            json.dump(node_des, f, ensure_ascii=False)

        with open(
                "D:\work\project\implementation\HT-kg-platform\kg-compute\\network-x\data\kg_data\\480318500696793088\\triples.json",
                "w", encoding="utf-8") as f:
            json.dump(ed, f, ensure_ascii=False)

        # 统计数值化属性的分布
        statistic_attribute = {}
        # 复杂度m*n
        for rule in param["graph_rules"]["attributes"]:
            if rule["value_type"] == "NUMERICAL":
                value_list = []
                for k in read_nodes.keys():
                    if rule["attribute_id"] in read_nodes[k].keys():
                        if not read_nodes[k][rule["attribute_id"]]:
                            continue
                        value_list.append(float(read_nodes[k][rule["attribute_id"]]))
                for k in ed.keys():
                    if rule["attribute_id"] in ed[k]["attributes"].keys():
                        if not ed[k]["attributes"][rule["attribute_id"]]:
                            continue
                        value_list.append(float(ed[k]["attributes"][rule["attribute_id"]]))
                statistic_attribute[rule["attribute_id"]] = value_list

        # 图初始化
        G = nx.DiGraph()  # 0.1
        for k in read_nodes.keys():
            G.add_node(k, weights=0.1)
        for e in ed.keys():
            G.add_edge(ed[e]["start_entity"], ed[e]["end_entity"], weights=0.1)
            # G.add_edge(ed[e]["start_entity"], ed[e]["end_entity"], weights=0.77)

        """ 为节点和边计算权重"""
        # for k in list(read_nodes.keys())[2:]:
        # 为节点计算权重
        #################################################################################
        process_num = 4
        pool = Pool(processes=process_num)
        result = []
        for k in read_nodes.keys():
            result.append(pool.apply_async(weights_evaluation, (
                'node', k, read_nodes[k], param, statistic_attribute, node_des[k],)))
        pool.close()
        pool.join()
        for i in result:
            (k,v) = i.get()
            G.nodes()[k]['weights'] = v
        ##################################################################################
        # for i in range(task_num):

        # for k in read_nodes.keys():
        # weights = dict(zip(read_nodes[k].keys(), [0.1] * len(read_nodes[k].keys())))
        # with Pool(processes=4) as pool:  # 开启4个工作进程
        #     G.nodes()[k]['weights'] = pool.apply(weights_evaluation, ['node',read_nodes[k],param,statistic_attribute,node_des[k]])  # 异步方式计算f(10)
        # G.nodes()[k]['weights'] = weights_evaluation('node',k)

        # for rule in param["graph_rules"]["attributes"]:
        #     for att in read_nodes[k]:
        #         if att == rule["attribute_id"] and node_des[k]["node_type_id"] == rule["type_id"]:
        #             # print("节点属性：", att)
        #             value = attributes_condition(read_nodes[k], rule, statistic_attribute)  #
        #             if value:
        #                 weights[att] = value
        #             # print("计算权重后的weights:", weights)
        #             # print("计算%s后的临时weights:", cal_weight(weights) %att)
        # w = cal_weight(weights)
        # # print("最终节点权重：", w)
        # G.nodes()[k]['weights'] = round(float(w), FLOAT_PRECESSION)

        # print()
        # print(statistic_attribute)
        # 为边计算权重
        for k in ed.keys():
            # print("关系数据：", ed[k])
            weights = dict(zip(ed[k]["attributes"].keys(), [0.1] * len(ed[k]["attributes"].keys())))
            if not weights:
                G.add_edge(ed[k]["start_entity"], ed[k]["end_entity"], weights=0.1)
                continue
            # with Pool(processes=4) as pool:  # 开启4个工作进程
            #     G.nodes()[k]['weights'] = pool.apply(weights_evaluation, ['edge',ed[k],param,statistic_attribute])  # 异步方式计算f(10)
            for rule in param["graph_rules"]["attributes"]:
                # 规则分类
                for att in ed[k]["attributes"].keys():
                    if att == rule["attribute_id"] and ed[k]["edge_type_id"] == rule["type_id"]:
                        # print(ed[k]["attributes"]["type_id"], ": 边属性：", att)
                        value = attributes_condition(ed[k]["attributes"], rule, statistic_attribute)  # 规则
                        if value:
                            weights[att] = value
                        # print("计算权重后的weights:", weights)

            # 边直接赋值

            # print("计算权重后的weights:", weights)
            w = cal_weight(weights)  # weight建模
            for rule in param["graph_rules"]["relations"]:
                if ed[k]["edge_type_id"] == rule["relation_id"]:
                    w = rule['weight_subject_to'][0]
            w = round(w, FLOAT_PRECESSION)
            # print("计算后的最终weight", w)
            if (ed[k]["start_entity"], ed[k]["end_entity"]) in G.edges():
                w = max(G.edges()[ed[k]["start_entity"], ed[k]["end_entity"]]['weights'], w)
            G.add_edge(ed[k]["start_entity"], ed[k]["end_entity"], weights=w)

            # G.add_edge(ed[k]["start_entity"], ed[k]["end_entity"], weights=w, label={"attr1": 2, "attr2": 2})
            # G.get_edge_data()
            # G.add_edge(ed[k]["start_entity"], ed[k]["end_entity"], weights=w)
            print()
        print("======================== 绘图 ========================")
        # pos = nx.random_layout(G)
        # _weights = nx.get_edge_attributes(G, "weights")
        # nx.draw_networkx(G, pos, with_labels=True)
        # nx.draw_networkx_edge_labels(G, pos, edge_labels=_weights)
        # plt.show()

        print("======================== 节点及其权重 ========================")
        # print(G.nodes(data=True))
        for n in G.nodes(data=True):
            print(n, node_des[n[0]]["name"])
            pass

        personal = {}
        for n in G.nodes(data=True):
            personal[n[0]] = n[1]["weights"]

            print()
        print("======================== 边及其权重 ========================")
        for _ in G.edges(data=True):
            print(_, node_des[_[0]]["name"], node_des[_[1]]["name"])

        pr = nx.pagerank(G, weight="weights", personalization=personal, alpha=alpha, max_iter=max_iter)
        sorted_pagerank = sorted(pr.items(), key=lambda x: x[1], reverse=True)

        num = min(len(sorted_pagerank), topk)

        result = []
        for _ in sorted_pagerank:
            return_node_type = param["return_node_type"]["entity_type_ids"] + param["return_node_type"][
                "event_type_ids"]
            if len(return_node_type) > 0:
                if node_des[_[0]]["node_type_id"] in return_node_type:
                    result.append({"id": _[0],
                                   "name": node_des[_[0]]["name"],
                                   "node_type": node_des[_[0]]["node_type"],
                                   "node_type_id": node_des[_[0]]["node_type_id"],
                                   "weight": round(_[1], FLOAT_PRECESSION)})
                else:
                    pass
            else:
                result.append({"id": _[0],
                               "name": node_des[_[0]]["name"],
                               "node_type": node_des[_[0]]["node_type"],
                               "node_type_id": node_des[_[0]]["node_type_id"],
                               "weight": round(_[1], FLOAT_PRECESSION)})
        result = result[:num]
        print("pr:", pr)
        print(num)
        print(result)

        return result

    except Exception as e:
        print(e)
        raise Exception(e)


def convert_attribute(d):
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


def cal_weight(weights, alpha=0.95, beta=1):
    # result = 0
    # for w in weights:
    #     if abs(weights[w] - 0.1) < 1e-5:
    #         result += weights[w]
    #     else:
    #         result += (weights[w] * (1+alpha)) ** beta
    # result /= len(weights)
    result = np.mean(list(weights.values()))
    return result


def attributes_condition(node, condition_dict, statistic_attribute):
    if condition_dict['type'] in ['ENTITY', "EVENT", "RELATION"]:
        if condition_dict["value_type"] == "CHARACTER":
            if condition_dict["rule"] == "EQ":
                if node[condition_dict["attribute_id"]] == condition_dict["rule_subject_to"][0]:
                    return condition_dict['weight_subject_to'][0]
            elif condition_dict["rule"] == "CONTAINS":
                if condition_dict["rule_subject_to"][0] in node[condition_dict["attribute_id"]]:
                    return condition_dict['weight_subject_to'][0]
            elif condition_dict["rule"] in ["ASCENDING", "DESCENDING"]:
                [_min, _max] = condition_dict['weight_subject_to']
                _min = 0.1 if abs(_min - 0.1) <= 1e-5 else _min

                length = len(condition_dict["rule_subject_to"])
                inter = (_max - _min) / (length - 1)
                new_condition = []
                for i in range(length):
                    new_condition.append(_min + i * inter)
                if condition_dict["rule"] == "ASCENDING":
                    return new_condition[
                        condition_dict["rule_subject_to"].index(node[condition_dict["attribute_id"]])]
                else:
                    a = condition_dict["rule_subject_to"].index(node[condition_dict["attribute_id"]])
                    return new_condition[
                        length - 1 - condition_dict["rule_subject_to"].index(node[condition_dict["attribute_id"]])]

        if condition_dict["value_type"] == "NUMERICAL":
            condition_dict["rule_subject_to"] = [float(_) for _ in condition_dict["rule_subject_to"]]
            if not node[condition_dict["attribute_id"]]:
                return None
            if condition_dict["rule"] == "BETWEEN":
                if condition_dict["rule_subject_to"][0] <= float(node[condition_dict["attribute_id"]]) <= \
                        condition_dict["rule_subject_to"][1]:
                    return condition_dict['weight_subject_to'][0]
            elif condition_dict["rule"] == "GT":
                if float(node[condition_dict["attribute_id"]]) > condition_dict["rule_subject_to"][0]:
                    return condition_dict['weight_subject_to'][0]
            elif condition_dict["rule"] == "LT":
                if float(node[condition_dict["attribute_id"]]) < condition_dict["rule_subject_to"][0]:
                    return condition_dict['weight_subject_to'][0]
            elif condition_dict["rule"] == "GEQ":
                if float(node[condition_dict["attribute_id"]]) >= condition_dict["rule_subject_to"][0]:
                    return condition_dict['weight_subject_to'][0]
            elif condition_dict["rule"] == "LEQ":
                if float(node[condition_dict["attribute_id"]]) <= condition_dict["rule_subject_to"][0]:
                    return condition_dict['weight_subject_to'][0]
            elif condition_dict["rule"] == "EQ":
                if abs(float(node[condition_dict["attribute_id"]]) - condition_dict["rule_subject_to"][0]) < 1e-5:
                    return condition_dict['weight_subject_to'][0]
            elif condition_dict["rule"] in ["DESCENDING", "ASCENDING"]:
                sort_list = statistic_attribute[condition_dict["attribute_id"]]
                sort_list.sort()
                sort_list = np.array(sort_list)
                mean = sort_list.mean()
                std = sort_list.std()
                sort_list = (sort_list - mean) / std
                temp = (float(node[condition_dict["attribute_id"]]) - mean) / std
                if abs(max(sort_list) - min(sort_list)) < 1e-5:
                    return 0.1
                r = (temp - min(sort_list)) / (max(sort_list) - min(sort_list)) * (
                        condition_dict['weight_subject_to'][1] - condition_dict['weight_subject_to'][0])
                r = round(r, FLOAT_PRECESSION)

                if r > 1 or r < 0:
                    print("z-score problem!!!", r)
                if condition_dict["rule"] == "DESCENDING":
                    if abs(1 - r) < 1e-5:
                        r = 0.9
                    return 1 - r
                else:
                    if abs(r) < 1e-5:
                        r = 0.1
                    return r
    return None


def relation_condition(edge, condition_dict):
    return condition_dict['weight_subject_to'][0]


if __name__ == '__main__':
    with open("main/temp/pagerank_data_params.json", "r", encoding="utf-8") as f:
        p = json.load(f)

    # 452120393941295104    480318500696793088 477487724460548096
    personal_pagerank(kg_name="480318500696793088", space_name="480318500696793088", alpha=0.85, max_iter=100, topk=5,
                      param=p)
