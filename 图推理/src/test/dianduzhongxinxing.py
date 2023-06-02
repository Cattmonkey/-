# -*- coding:utf-8 -*-
import time

import networkx as nx

g = nx.MultiGraph()
g.add_edge("1", "2", weight=0.2)
g.add_edge("1", "2", weight=0.2)
g.add_edge("1", "2", weight=0.5)
g.add_edge("5", "2", weight=0.2)
g.add_edge("6", "2", weight=0.2)
g.add_edge("3", "2", weight=0.2)
g.add_edge("4", "2", weight=0.2)

# a = nx.pagerank(g, weight="weight")
# print(a)
# c = nx.algorithms.community.greedy_modularity_communities(g, weight="weight")
# print(c)
s = time.time()
d = nx.centrality.degree_centrality(g)
e = time.time()
print(e-s)
print(d)