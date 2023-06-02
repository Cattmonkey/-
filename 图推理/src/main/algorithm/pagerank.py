# -*- coding:utf-8 -*-
import json

import networkx as nx

from graph_data import read_graph_data

FLOAT_PRECESSION = 5


def personal_pagerank(kg_name, space_name, alpha, max_iter, topk, params):
    G, nodes_data, edges_data, _ = read_graph_data(space_name, kg_name, params["graph_rules"], direction=True,
                                                   edge_function="avg")

    personal = {}
    for n in G.nodes(data=True):
        personal[n[0]] = n[1]["weights"]

    pr = nx.pagerank(G, weight="weights", personalization=personal, alpha=alpha, max_iter=max_iter)
    sorted_pagerank = sorted(pr.items(), key=lambda x: x[1], reverse=True)

    num = min(len(sorted_pagerank), topk)

    result = []
    return_node_type = params["return_node_type"]["entity_type_ids"] + params["return_node_type"][
        "event_type_ids"]
    for _ in sorted_pagerank:
        if len(return_node_type) > 0:
            if nodes_data[_[0]]["node_type_id"] in return_node_type:
                result.append({"id": _[0],
                               "name": nodes_data[_[0]]["name"],
                               "node_type": nodes_data[_[0]]["node_type"],
                               "node_type_id": nodes_data[_[0]]["node_type_id"],
                               "weight": round(_[1], FLOAT_PRECESSION)})
            else:
                pass
        else:
            result.append({"id": _[0],
                           "name": nodes_data[_[0]]["name"],
                           "node_type": nodes_data[_[0]]["node_type"],
                           "node_type_id": nodes_data[_[0]]["node_type_id"],
                           "weight": round(_[1], FLOAT_PRECESSION)})
    result = result[:num]
    print("pr:", pr)
    print(result)

    nodes = [_["id"] for _ in result]
    statistics_info = interpretability_analysis(G, nodes_data, personal, nodes)

    return result, statistics_info


def interpretability_analysis(G, nodes_data, personal, nodes):
    in_degree = {}
    self_weight = {}

    for item in G.in_degree:
        if item[0] in nodes:
            in_degree.update({item[0]: item[1]})
            self_weight.update({item[0]: personal[item[0]]})

    sorted_in_degree = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)
    sorted_self_weight = sorted(self_weight.items(), key=lambda x: x[1], reverse=True)

    sorted_in_degree = [{"id": _[0], "name": nodes_data[_[0]]["name"], "in_degree": _[1]} for _ in sorted_in_degree]
    sorted_self_weight = [{"id": _[0], "name": nodes_data[_[0]]["name"], "self-weight": _[1]} for _ in
                          sorted_self_weight]

    return {"in_degree_analysis": sorted_in_degree, "self_weight_analysis": sorted_self_weight}


if __name__ == '__main__':
    pass
    with open("../temp/pagerank_data_params.json", "r", encoding="utf-8") as f:
        p = json.load(f)

    # 452120393941295104    480318500696793088 477487724460548096
    personal_pagerank(kg_name="480318500696793088", space_name="480318500696793088", alpha=0.85, max_iter=100, topk=5,
                      params=p)
