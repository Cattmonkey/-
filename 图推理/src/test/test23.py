# -*- coding:utf-8 -*-
import networkx as nx


def interpretability_analysis(G, nodes_data, main_node, other_nodes):
    main_node_neighbors = set(G.neighbors(main_node))
    com_neighbors = {}
    shortest_path_lengths = {}
    for other in other_nodes:
        other_neighbors = set(G.neighbors(other))
        com = main_node_neighbors & other_neighbors
        com_neighbors[other] = len(com)
        path_length = nx.shortest_path_length(G, source=main_node, target=other)
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


g = nx.Graph()
g.add_edge("1", "4", weight=0.1)
g.add_edge("1", "6", weight=0.1)
g.add_edge("1", "5", weight=0.1)
g.add_edge("4", "5", weight=0.1)
g.add_edge("4", "6", weight=0.1)
g.add_edge("4", "2", weight=0.1)
g.add_edge("4", "3", weight=0.1)
g.add_edge("3", "2", weight=0.1)

node = "4"
pairs = []
for n in g:
    if n != node:
        pairs.append((node, n))

cnc = nx.common_neighbor_centrality(g, ebunch=pairs, alpha=0.8)

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
        "v_node_name": v_node[i],
        "value": p_value[i]
    })

topk = 10

result = {"m_node": node,
          "m_node_name": node,
          "relations": relations[:topk]
          }

print(result)
other_nodes = [_["v_node"] for _ in result["relations"]]
# statistics_info = interpretability_analysis(g, "nodes_data", node, other_nodes)


print("4,1共有邻居：", set(g.neighbors("4")) & set(g.neighbors("1")))
print("4,1距离：", nx.shortest_path_length(g, source="4", target="1"))

print("4,3共有邻居：", set(g.neighbors("4")) & set(g.neighbors("3")))
print("4,3距离：", nx.shortest_path_length(g, source="4", target="3"))

