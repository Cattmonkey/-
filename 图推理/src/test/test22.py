# -*- coding:utf-8 -*-
import networkx as nx

g = nx.DiGraph()
g.add_edge("1", "2", weight=0.1)
# g.add_edge("1", "2", weight=0.2)
# g.add_edge("1", "2", weight=0.5)
g.add_edge("1", "3", weight=0.1)
g.add_edge("4", "1", weight=0.1)
g.add_edge("5", "1", weight=0.1)
g.add_edge("1", "3", weight=0.1)

personalization = {"1": 0.1, "2": 0.3, "3": 0.2, "4": 0.6, "5": 0.1}

a = nx.pagerank(g, personalization=personalization, weight="weight")
print(a)
print(g.in_degree)
# c = nx.algorithms.community.greedy_modularity_communities(g, weight="weight")
# print(c)


# g = nx.Graph()
# g.add_edge("3", "2", weight=0.1)
# g.add_edge("3", "5", weight=0.1)
# g.add_edge("3", "4", weight=0.1)
# g.add_edge("4", "1", weight=0.1)
# g.add_edge("4", "2", weight=0.1)
# g.add_edge("4", "5", weight=0.1)
# g.add_edge("5", "1", weight=0.1)
#
# nx.common_neighbor_centrality(g,ebunch=[("")])
