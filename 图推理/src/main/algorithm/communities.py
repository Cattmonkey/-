# -*- coding:utf-8 -*-
import json

import networkx as nx

from graph_data import read_graph_data


def personal_communities(kg_name, space_name, params, weight=None, resolution=1, cutoff=1, best_n=None):
    G, nodes_data, edges_data, _ = read_graph_data(space_name, kg_name, params["graph_rules"], direction=False,
                                                   edge_function="avg")
    communities = nx.algorithms.community.greedy_modularity_communities(G, weight=weight, resolution=resolution,
                                                                        cutoff=cutoff, best_n=best_n)
    result = []

    for _ in communities:
        temp = []
        for i in _:
            temp.append({"id": i,
                         "name": nodes_data[i]["name"],
                         "node_type": nodes_data[i]["node_type"],
                         "node_type_id": nodes_data[i]["node_type_id"]})
        result.append(temp)

    statistics_info = interpretability_analysis(G, communities)
    return result, statistics_info


def interpretability_analysis(G, communities):
    compairs = dict(enumerate(communities))
    compairs2 = []
    for c in communities:
        adj_list = set()
        for n in c:
            adj = G.adj[n]
            for i in adj.keys():
                adj_list.add(i)
        compairs2.append(adj_list)
    compairs2 = dict(enumerate(compairs2))

    result = []
    for i in range(len(compairs)):
        temp = []
        for j in range(len(compairs2)):
            temp.append(len(compairs[i] & compairs2[j]) / len(compairs[i]))

    return {"concentration_matrix": result}


if __name__ == '__main__':
    with open("../temp/pagerank_data_params.json", "r", encoding="utf-8") as f:
        p = json.load(f)
    personal_communities(kg_name="480318500696793088", space_name="480318500696793088", params=p)
