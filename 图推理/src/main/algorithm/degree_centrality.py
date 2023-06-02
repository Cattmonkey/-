# -*- coding:utf-8 -*-
import networkx as nx

from graph_data import read_graph_data

FLOAT_PRECESSION = 5


def degree_centrality(kg_name, space_name, topk, params):
    G, nodes_data, edges_data, _ = read_graph_data(space_name, kg_name, params["graph_rules"], direction=False,
                                                   edge_function="avg")

    degree_centrality = nx.centrality.degree_centrality(G)

    sorted_degree_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)

    num = min(len(sorted_degree_centrality), topk)

    result = []
    for _ in sorted_degree_centrality:
        return_node_type = params["return_node_type"]["entity_type_ids"] + params["return_node_type"][
            "event_type_ids"]
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
    # print("degree_centrality:", degree_centrality)
    print(result)

    nodes = [_["id"] for _ in result]
    statistics_info = interpretability_analysis(G, nodes_data, nodes)

    return result, statistics_info


def interpretability_analysis(G, nodes_data, nodes):
    degree = {}

    for item in G.degree:
        if item[0] in nodes:
            degree.update({item[0]: item[1]})

    sorted_degree = sorted(degree.items(), key=lambda x: x[1], reverse=True)

    sorted_degree = [{"id": _[0], "name": nodes_data[_[0]]["name"], "degree": _[1]} for _ in sorted_degree]

    return {"degree_analysis": sorted_degree}


if __name__ == '__main__':
    a = {"space_name": "480318500696793088", "kg_name": "480328893322272768", "node": "480332111502680064",
         "alpha": 0.85,
         "topk": 10, "return_node_type": {"entity_type_ids": [], "event_type_ids": []}, "graph_rules": {"attributes": [
            {"type": "ENTITY", "type_id": "480318595559366656", "attribute_id": "480400114604875776",
             "value_type": "NUMERICAL", "rule": "GT", "rule_subject_to": ["34"], "weight_subject_to": [0.2]}],
            "relations": []}}
    x = degree_centrality(kg_name="480328893322272768", space_name="480318500696793088", topk=10, params=a)

    print(x)
