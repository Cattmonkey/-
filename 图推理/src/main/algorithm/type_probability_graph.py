# -*- coding:utf-8 -*-

from graph_data import read_graph_data

FLOAT_PRECESSION = 5


def type_probability_graph(kg_name, space_name, type_filter, params):
    g, nodes_data, edges_data, _ = read_graph_data(space_name, kg_name, params["graph_rules"], direction=False,
                                                   edge_function="avg")
    node_type_statistic = {}
    for node in g.nodes():
        node_type_id = nodes_data[node]["node_type_id"]
        node_type = nodes_data[node]["node_type"]
        # 要求目标节点和其邻居节点都为事件节点
        if node_type in type_filter:
            node_neighbors = g.neighbors(node)
            node_neighbors = [_ for _ in node_neighbors if nodes_data[_]["node_type"] in type_filter]
            node_neighbors_type = [nodes_data[_]["node_type_id"] for _ in node_neighbors]
            if node_type not in node_type_statistic.keys():
                node_type_statistic[node_type_id] = node_neighbors_type
            else:
                node_type_statistic[node_type_id] = node_type_statistic[node_type_id] + node_neighbors_type

    print("======================================== 节点类型统计： ========================================")
    print(node_type_statistic)

    if len(node_type_statistic) == 0:
        pass

    result = []
    for key in node_type_statistic.keys():
        end_nodes = node_type_statistic[key]
        end_nodes_size = len(end_nodes)
        part = []
        for end_node in end_nodes:
            count = end_nodes.count(end_node)
            part.append({"start_node_type": key,
                         "end_node_type": end_node,
                         "probability": round(count / end_nodes_size, FLOAT_PRECESSION),
                         "end_node_type_count": count,
                         "end_nodes_size": end_nodes_size,
                         "end_nodes": end_nodes
                         })
        result.append(part)

    print("======================================== 节点类型概率： ========================================")
    print(result)
    statistics_info = {}
    return result, statistics_info


if __name__ == '__main__':
    pass
    p = {"space_name": "480318500696793088", "kg_name": "480328893322272768", "node": "480332111502680064",
         "alpha": 0.8,
         "topk": 10, "return_node_type": {"entity_type_ids": [], "event_type_ids": []}, "graph_rules": {"attributes": [
            {"type": "ENTITY", "type_id": "480318595559366656", "attribute_id": "480400114604875776",
             "value_type": "NUMERICAL", "rule": "GT", "rule_subject_to": ["34"], "weight_subject_to": [0.2]}],
            "relations": []}}
    type_probability_graph(kg_name="480328893322272768", space_name="480318500696793088",
                           type_filter=["ENTITY", "EVENT"],
                           params=p)
