import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

feature_1 = ['Boston', 'Boston', 'Chicago', 'ATX', 'NYC']
feature_2 = ['LA', 'SFO', 'LA', 'ATX', 'NJ']
score = [1.00, 0.83, 0.34, 0.98, 0.89]

edges = [(feature_1[_], feature_2[_], score[_]) for _ in range(5)]
# print(df)

# edges = nx.from_pandas_edgelist(df=df, source="f1", target="f2", edge_attr="score")


g = nx.DiGraph()  # 定义有向图，无向图是nx.Graph()
g.add_weighted_edges_from(edges)
weights = g.edges.data("weight")
for k in weights:
    g.add_edge(k[0], k[1], weight=k[2])
# 生成节点位置序列
pos = nx.random_layout(g)
weights = nx.get_edge_attributes(g, "weight")
nx.draw_networkx(g, pos, with_labels=True)
nx.draw_networkx_edge_labels(g, pos, edge_labels=weights)
plt.show()
