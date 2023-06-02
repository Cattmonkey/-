# -*- coding:utf-8 -*-
import networkx as nx
import random
import time


# 创建有向图

d = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "X",
     "Y", "Z"]

edges = []
for n in range(3):
    d.extend([_ + str(n) + "*" for _ in d])

for i in d:
    for j in d:
        if i != j:
            edges.append((i, j))


time_ = []
for b in [1,10,20,50,100]:
    G = nx.DiGraph()
    e = []
    for i in range(b):
        e.extend([(_[0] + str(i), _[1] + str(i),) for _ in edges])

    print("边数量")
    print(len(e))
    G.add_edges_from(e)
    nx.draw(G, with_labels=True)
    start = time.time()
    pagerank_list = nx.pagerank(G, alpha=0.85)
    end = time.time()
    print(end-start)
    time_.append(end-start)
    print(pagerank_list)


print("time序列")
print(time_)
# edges = [("A", "B"), ("A", "C"), ("A", "D"),
#          ("B", "A"), ("B", "D"), ("C", "A"),
#          ("D", "B"), ("D", "C")]
# 有向图边之间的关系


# G.add_edges_from(edges)
# 根据连边构造图

#
# nx.draw(G, with_labels=True)
# start = time.time()
# pagerank_list = nx.pagerank(G, alpha=0.85)
# end = time.time()
# print(pagerank_list)
# '''
# {'A': 0.3245609358176831,
#  'B': 0.22514635472743894,
#  'C': 0.22514635472743894,
#  'D': 0.22514635472743894}
#  '''
