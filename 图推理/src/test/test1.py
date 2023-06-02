# -*- coding:utf-8 -*-
import networkx as nx
import random
import time


# 创建有向图

d = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "X",
     "Y", "Z"]

edges = [("华盛顿号航空母舰","F18舰载机"),("华盛顿号航空母舰",""
                                           "横须贺海军基地")]




G = nx.DiGraph()


print("边数量")
G.add_edges_from(edges)
nx.draw(G, with_labels=True)
start = time.time()
pagerank_list = nx.pagerank(G, alpha=0.85)
end = time.time()
print(end-start)
print(pagerank_list)

