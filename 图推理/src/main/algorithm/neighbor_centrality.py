# -*- coding:utf-8 -*-
import networkx as nx

from graph_data import read_graph_data

FLOAT_PRECESSION = 5


def common_neighbor_centrality(kg_name, space_name, node, alpha, topk, params):
    G, nodes_data, edges_data, _ = read_graph_data(space_name, kg_name, params["graph_rules"], direction=False,
                                                   edge_function="avg")

    pairs = []
    for n in G:
        if n != node and G.has_edge(node, n):
            pairs.append((node, n))
    if len(pairs) < 1:
        result = {"id": node, "name": nodes_data[node]["name"], "correlation_info": []}
        statistics_info = {"com_neighbors_analysis": [], "shortest_path_lengths_analysis": []}
        return result, statistics_info

    cnc = nx.common_neighbor_centrality(G, ebunch=pairs, alpha=alpha)

    # pos = nx.random_layout(G)
    # _weights = nx.get_edge_attributes(G, "weights")
    # nx.draw_networkx(G, pos, with_labels=True)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=_weights)
    # plt.show()

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
    return_node_type = params["return_node_type"]["entity_type_ids"] + params["return_node_type"][
        "event_type_ids"]
    for i in sorted_inds:
        if len(return_node_type) > 0:
            if nodes_data[v_node[i]]["node_type_id"] in return_node_type:
                relations.append({
                    "id": v_node[i],
                    "name": nodes_data[v_node[i]]["name"],
                    "value": p_value[i],
                    "node_type": nodes_data[v_node[i]]["node_type"],
                    "node_type_id": nodes_data[v_node[i]]["node_type_id"],
                })
            else:
                pass
        else:
            relations.append({
                "id": v_node[i],
                "name": nodes_data[v_node[i]]["name"],
                "value": p_value[i],
                "node_type": nodes_data[v_node[i]]["node_type"],
                "node_type_id": nodes_data[v_node[i]]["node_type_id"],
            })


    topk = min(topk, len(relations))

    result = {"id": node,
              "name": nodes_data[node]["name"],
              "correlation_info": relations[:topk]
              }

    print(result)
    other_nodes = [_["id"] for _ in result["correlation_info"]]
    statistics_info = interpretability_analysis(G, nodes_data, node, other_nodes)
    return result, statistics_info


def interpretability_analysis(G, nodes_data, main_node, other_nodes):
    main_node_neighbors = set(G.neighbors(main_node))
    com_neighbors = {}
    shortest_path_lengths = {}
    for other in other_nodes:
        other_neighbors = set(G.neighbors(other))
        com = main_node_neighbors & other_neighbors
        com_neighbors[other] = len(com)
        path_length = nx.shortest_path_length(G, source=main_node, target=other, weight="weight")
        shortest_path_lengths[other] = path_length
    sorted_com_neighbors = sorted(com_neighbors.items(), key=lambda x: x[1], reverse=True)

    sorted_com_neighbors = [{"id": _[0], "name": nodes_data[_[0]]["name"], "com_neighbors": _[1]} for _ in
                            sorted_com_neighbors]

    print(sorted_com_neighbors)

    sorted_shortest_path_lengths = sorted(shortest_path_lengths.items(), key=lambda x: x[1], reverse=False)

    sorted_shortest_path_lengths = [{"id": _[0], "name": nodes_data[_[0]]["name"], "shortest_path_length": _[1]} for _
                                    in
                                    sorted_shortest_path_lengths]
    result = {"com_neighbors_analysis": sorted_com_neighbors,
              "shortest_path_lengths_analysis": sorted_shortest_path_lengths}

    return result


if __name__ == '__main__':
    a = {"space_name": "480318500696793088", "kg_name": "480328893322272768", "node": "480332111502680064",
         "alpha": 0.85,
         "topk": 10, "return_node_type": {"entity_type_ids": [], "event_type_ids": []}, "graph_rules": {"attributes": [
            {"type": "ENTITY", "type_id": "480318595559366656", "attribute_id": "480400114604875776",
             "value_type": "NUMERICAL", "rule": "GT", "rule_subject_to": ["34"], "weight_subject_to": [0.2]}],
            "relations": []}}
    x = common_neighbor_centrality(kg_name="482933010691563520", space_name="482931410182905856",
                                   node="482933131818868736", alpha=0.8, topk=10, params=a)
