# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt

import networkx as nx
import numpy as np

G = nx.DiGraph()

# G.add_weighted_edges_from([("A", "B", 2),
#                            ("A", "C", 10),
#                            ("C", "D", 2000),
#                            ("C", "B", 2),
#                            ])
G.add_weighted_edges_from([("A", "A", 0.1),
                           ("E", "A", 0.1),
                           ("C", "A", 0.1),
                           ("B", "A", 0.1),
                           ("F", "B", 0.1),
                           ("D", "B", 0.1),
                           ("D", "A", 0.1),
                           ])

pos = nx.random_layout(G)
_weights = nx.get_edge_attributes(G, "weights")
nx.draw_networkx(G, pos, with_labels=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=_weights)
plt.show()
pr = nx.pagerank(G)
print(pr)
print(np.sum(list(pr.values())))
prp = nx.pagerank(G, personalization={"A": 0.1, "B": 0.1, "C": 0.1, "D": 0.1, "E": 0.1, "F": 0.1, })

# print(prp)
# print(np.sum(list(prp.values())))
