# -*- coding:utf-8 -*-
import json
import os.path

import networkx as nx
import numpy as np
from nebula3.Config import Config
from nebula3.gclient.net import ConnectionPool

from config import KG_SOURCE_CONFIG
from tools.file_process import FileProcess
from tools.path import PathTools

GRAPH = {}


def data_synchronization(kg_name):
    kg_save_path = PathTools.PROJECT_ROOT + "data/kg_data/%s" % kg_name
    if not os.path.exists(kg_save_path):
        PathTools.makedirs(kg_save_path)
    status = {"status": "start"}
    FileProcess.save_json(status, kg_save_path + "/status.json")

    """从图数据库读取数据"""
    status = {"status": "synchronizing"}
    FileProcess.save_json(status, kg_save_path + "/status.json")
    try:
        di_graph = nx.DiGraph()
        no_graph = nx.Graph()

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
        session.execute('USE `%s`' % kg_name)
        # 执行查看TAG命令
        result = session.execute('SHOW TAGS')
        print(result)
        edges = []
        vertex_map = dict()
        # nodes_sql = "MATCH (v) return v LIMIT 10000"
        # try:
        #     sts = json.loads(session.execute_json(nodes_sql))
        # except Exception as e:
        #     print("查询节点数据错误！")
        #     print(e)
        # try:
        #     if sts["errors"][0]["code"] == 0:
        #         rows = sts["results"][0]['data']
        #         for r in rows:
        #             attributes = r["row"][0]
        #             attribute_ids = [_ for _ in attributes.keys() if ("name" not in _ and "graphId" not in _)]
        #             S_name_key = [_ for _ in attributes.keys() if "name" in _][0]
        #             S_id_key = [_ for _ in attributes.keys() if "graphId" in _][0]
        #             S_name = attributes[S_name_key]
        #             S_id = S_id_key.replace(".graphId", "")
        #             for a_id in attribute_ids:
        #                 attribute = attributes[a_id]
        #                 if attribute:
        #                     print("属性：%s" % attribute)
        #                     edge_weight = 0.5
        #                     edges.append((S_id, attribute, edge_weight))
        #                     vertex_map[S_id] = S_name
        #
        # except Exception as e:
        #     print(e)

        edges_id = session.execute('SHOW EDGES')
        for i in range(len(edges_id.rows())):
            e_id = str(edges_id.row_values(i)[0]).replace("\"", "")
            sql = "MATCH p=(v1)-[e:`%s`]-(v2) return p" % e_id
            try:
                spo = json.loads(session.execute_json(sql))
            except Exception as e:
                print("查询数据错误！")
                print(e)
            try:
                if spo["errors"][0]["code"] == 0:
                    rows = spo["results"][0]['data']
                    for r in rows:
                        # print(r)
                        meta = r["meta"][0]
                        row = r["row"][0]
                        # S_id = meta[1]["id"]["src"]
                        # O_id = meta[1]["id"]["dst"]
                        S_name_key = [_ for _ in row[0].keys() if "name" in _][0]
                        S_id_key = [_ for _ in row[0].keys() if "graphId" in _][0]
                        S_name = row[0][S_name_key]
                        S_id = S_id_key.replace(".graphId", "")

                        O_name_key = [_ for _ in row[2].keys() if "name" in _][0]
                        O_id_key = [_ for _ in row[2].keys() if "graphId" in _][0]
                        O_name = row[2][O_name_key]
                        O_id = O_id_key.replace(".graphId", "")
                        # todo 配置权重
                        edge_weight = 0.5
                        edges.append((S_id, O_id, edge_weight))
                        vertex_map[S_id] = S_name
                        vertex_map[O_id] = O_name

            except Exception as e:
                print(e)

        # 释放会话
        session.release()

        # 关闭连接池
        connection_pool.close()
        """以上是数据库链接"""

        # edges = read_local(PathTools.PROJECT_ROOT + "/data/test/military.json")
        # # edges=[]
        print("edges数量！")
        print(len(edges))
        di_graph.add_weighted_edges_from(edges)
        no_graph.add_weighted_edges_from(edges)
        #
        nx.write_gml(di_graph, kg_save_path + "/%s.gml" % kg_name)
        nx.write_gml(no_graph, kg_save_path + "/no_%s.gml" % kg_name)
        FileProcess.save_json(vertex_map, kg_save_path + "/%s-vertex_map.json" % kg_name)

    except Exception as e:
        print(e)
        status = {"status": "error"}
        FileProcess.save_json(status, kg_save_path + "/status.json")

    status = {"status": "completed"}
    FileProcess.save_json(status, kg_save_path + "/status.json")


def data_synchronization_status(kg_name):
    kg_save_path = PathTools.PROJECT_ROOT + "data/kg_data/%s" % kg_name
    if not os.path.exists(kg_save_path + "/status.json"):
        return False
    else:
        status = FileProcess.read_json(kg_save_path + "/status.json")
        return status


def page_rank(kg_name, alpha, max_iter, topk):
    if kg_name not in GRAPH.keys():
        model = {
            "model": nx.read_gml(PathTools.PROJECT_ROOT + "data/kg_data/%s/%s.gml" % (kg_name, kg_name)),
            "no_model": nx.read_gml(PathTools.PROJECT_ROOT + "data/kg_data/%s/no_%s.gml" % (kg_name, kg_name)),
            "param": FileProcess.read_json(
                PathTools.PROJECT_ROOT + "data/kg_data/%s/%s-vertex_map.json" % (kg_name, kg_name))
        }
        GRAPH[kg_name] = model

    if "no_model" not in GRAPH[kg_name].keys():
        GRAPH[kg_name]["no_model"] = nx.read_gml(
            PathTools.PROJECT_ROOT + "data/kg_data/%s/no_%s.gml" % (kg_name, kg_name))
    pagerank = nx.pagerank(GRAPH[kg_name]["model"], alpha=alpha, max_iter=max_iter)
    sorted_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)

    num = min(len(sorted_pagerank), topk)

    result = []
    for _ in sorted_pagerank[:num]:
        result.append({"id": _[0], "weight": _[1], "name": GRAPH[kg_name]["param"][_[0]]})

    return result


def release_kg(kg_name):
    try:
        if kg_name in GRAPH.keys():
            del GRAPH[kg_name]
        return True
    except Exception:
        return False


def read_local(file):
    data = []
    with open(file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = json.loads(line)
            main_key = "名称"
            for key in line.keys():
                if key not in [main_key, "_id", "图片", "简介"]:
                    S = line[main_key].strip()
                    O = line[key].strip()
                    if S == "" or O == "":
                        pass
                    else:
                        data.append((S, O, 0.5))
    return data


def asyn_lpa_communities(kg_name, weight=None, seed=None):
    if kg_name not in GRAPH.keys():
        model = {
            "model": nx.read_gml(PathTools.PROJECT_ROOT + "data/kg_data/%s/%s.gml" % (kg_name, kg_name)),
            "no_model": nx.read_gml(PathTools.PROJECT_ROOT + "data/kg_data/%s/no_%s.gml" % (kg_name, kg_name)),
            "param": FileProcess.read_json(
                PathTools.PROJECT_ROOT + "data/kg_data/%s/%s-vertex_map.json" % (kg_name, kg_name))
        }
        GRAPH[kg_name] = model

    if "no_model" not in GRAPH[kg_name].keys():
        GRAPH[kg_name]["no_model"] = nx.read_gml(
            PathTools.PROJECT_ROOT + "data/kg_data/%s/no_%s.gml" % (kg_name, kg_name))

    lpa = nx.algorithms.community.asyn_lpa_communities(GRAPH[kg_name]["model"], weight=weight, seed=seed)
    result = []
    for entity_set in lpa:
        result.append([{_: GRAPH[kg_name]["param"][_]} for _ in list(entity_set)])
    # result.insert(0, len(result))
    # print(result)
    result = dict(enumerate(result))

    return result


def common_neighbor_centrality(kg_name, node, alpha, topk):
    if kg_name not in GRAPH.keys():
        model = {
            "model": nx.read_gml(PathTools.PROJECT_ROOT + "data/kg_data/%s/%s.gml" % (kg_name, kg_name)),
            "no_model": nx.read_gml(PathTools.PROJECT_ROOT + "data/kg_data/%s/no_%s.gml" % (kg_name, kg_name)),
            "param": FileProcess.read_json(
                PathTools.PROJECT_ROOT + "data/kg_data/%s/%s-vertex_map.json" % (kg_name, kg_name))
        }
        GRAPH[kg_name] = model

    if "no_model" not in GRAPH[kg_name].keys():
        GRAPH[kg_name]["no_model"] = nx.read_gml(
            PathTools.PROJECT_ROOT + "data/kg_data/%s/no_%s.gml" % (kg_name, kg_name))
    pairs = []
    for n in GRAPH[kg_name]["no_model"]:
        if n != node:
            pairs.append((node, n))
    cnc = nx.common_neighbor_centrality(GRAPH[kg_name]["no_model"], ebunch=pairs, alpha=alpha)

    u_node = []
    v_node = []
    p_value = []
    for u, v, p in cnc:
        u_node.append(u)
        v_node.append(v)
        p_value.append(p)

    m_sorted = sorted(enumerate(p_value), key=lambda x: x[1], reverse=True)
    sorted_inds = [m[0] for m in m_sorted]

    relations = []
    for i in sorted_inds:
        relations.append({
            "v_node": v_node[i],
            "v_node_name": GRAPH[kg_name]["param"][v_node[i]],
            "value": p_value[i]

        })

    topk = min(topk, len(relations))

    result = {"m_node": node,
              "m_node_name": GRAPH[kg_name]["param"][node],
              "relations": relations[:topk]
              }
    return result


def shortest_path(kg_name, source=None, target=None, method="dijkstra"):
    if kg_name not in GRAPH.keys():
        model = {
            "model": nx.read_gml(PathTools.PROJECT_ROOT + "data/kg_data/%s/%s.gml" % (kg_name, kg_name)),
            "no_model": nx.read_gml(PathTools.PROJECT_ROOT + "data/kg_data/%s/no_%s.gml" % (kg_name, kg_name)),
            "param": FileProcess.read_json(
                PathTools.PROJECT_ROOT + "data/kg_data/%s/%s-vertex_map.json" % (kg_name, kg_name))
        }
        GRAPH[kg_name] = model

    if "no_model" not in GRAPH[kg_name].keys():
        GRAPH[kg_name]["no_model"] = nx.read_gml(
            PathTools.PROJECT_ROOT + "data/kg_data/%s/no_%s.gml" % (kg_name, kg_name))

    sp = nx.algorithms.shortest_paths.shortest_path(GRAPH[kg_name]["model"], source=source, target=target,
                                                    method=method)  # method = "bellman-ford","dijkstra"
    return sp


def simple_path(kg_name, source, target):
    if kg_name not in GRAPH.keys():
        model = {
            "model": nx.read_gml(PathTools.PROJECT_ROOT + "data/kg_data/%s/%s.gml" % (kg_name, kg_name)),
            "no_model": nx.read_gml(PathTools.PROJECT_ROOT + "data/kg_data/%s/no_%s.gml" % (kg_name, kg_name)),
            "param": FileProcess.read_json(
                PathTools.PROJECT_ROOT + "data/kg_data/%s/%s-vertex_map.json" % (kg_name, kg_name))
        }
        GRAPH[kg_name] = model

    if "no_model" not in GRAPH[kg_name].keys():
        GRAPH[kg_name]["no_model"] = nx.read_gml(
            PathTools.PROJECT_ROOT + "data/kg_data/%s/no_%s.gml" % (kg_name, kg_name))

    sp = nx.algorithms.shortest_simple_paths(GRAPH[kg_name]["model"], source=source, target=target)
    result = dict(enumerate(sp))
    return result


def graph_traversal(kg_name, source=None, depth_limit=None, method="dfs"):
    if kg_name not in GRAPH.keys():
        model = {
            "model": nx.read_gml(PathTools.PROJECT_ROOT + "data/kg_data/%s/%s.gml" % (kg_name, kg_name)),
            "no_model": nx.read_gml(PathTools.PROJECT_ROOT + "data/kg_data/%s/no_%s.gml" % (kg_name, kg_name)),
            "param": FileProcess.read_json(
                PathTools.PROJECT_ROOT + "data/kg_data/%s/%s-vertex_map.json" % (kg_name, kg_name))
        }
        GRAPH[kg_name] = model

    if "no_model" not in GRAPH[kg_name].keys():
        GRAPH[kg_name]["no_model"] = nx.read_gml(
            PathTools.PROJECT_ROOT + "data/kg_data/%s/no_%s.gml" % (kg_name, kg_name))
    if method == 'bfs':
        if source:
            r = nx.algorithms.traversal.bfs_edges(GRAPH[kg_name]["model"], source=source, depth_limit=depth_limit)
        else:
            print("Need a node specified.")
            return -1
    else:
        r = nx.algorithms.traversal.dfs_edges(GRAPH[kg_name], source=source, depth_limit=depth_limit)
    result = []
    for entity_set in r:
        result.append(list(entity_set))
    result = dict(enumerate(result))
    return result


if __name__ == '__main__':
    data_synchronization("452120393941295104")

    r = page_rank("452120393941295104", 0.85, 100, 10)
    #
    # print(len(r))
    test = ('452124161181261824', '452125364170563584')

    x = common_neighbor_centrality("452120393941295104", node="452124161181261824", alpha=0.8, topk=10)

    print(x)
    print()
    for i in x["relations"]:
        print(i)
