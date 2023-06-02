# -*- coding:utf-8 -*-
import networkx as nx
import json
from graph_data import read_graph_data


def shortest_path(kg_name, space_name, params, source=None, target=None, method="max", filter_event=False):
    G, nodes_data, edges_data, all_edges = read_graph_data(space_name, kg_name, params["graph_rules"],
                                                           direction=True,
                                                           edge_function="avg",
                                                           filter_event=filter_event)
    try:
        sp = nx.algorithms.shortest_paths.shortest_path(G, source=source,
                                                        target=target,
                                                        weight="weights")  # method = "bellman-ford","dijkstra"
    except nx.NetworkXNoPath as e:
        return []
    except nx.NodeNotFound as e:
        raise e
    print(sp)
    results = []
    for i in range(len(sp)):
        j = i + 1
        if j >= len(sp):
            break
        source_id = sp[i]
        source_name = nodes_data[source_id]['name']
        source_type = nodes_data[source_id]['node_type']
        source_type_id = nodes_data[source_id]['node_type_id']
        target_id = sp[j]
        target_name = nodes_data[target_id]['name']
        target_type = nodes_data[target_id]['node_type']
        target_type_id = nodes_data[target_id]['node_type_id']
        key = source_id + ',' + target_id
        dict_list = all_edges[key]

        edge = list()
        for k in dict_list:
            temp = list(list(k.items())[0])
            if edge:
                if method == 'max':
                    edge = temp if temp[1] > edge[1] else edge
                elif method == 'min':
                    edge = temp if temp[1] < edge[1] else edge
            else:
                edge = temp

        edge_id = edge[0]
        edge_type = edges_data[edge_id]['attributes']['edgeType']
        edge_type_id = edges_data[edge_id]['edge_type_id']
        edge_name = edges_data[edge_id]['name']

        direction = None if 'direction' not in edges_data[edge_id]['attributes'] else edges_data[edge_id]['attributes'][
            'direction']

        results.append({"source_id": source_id,
                        "source_name": source_name,
                        "source_type": source_type,
                        "source_type_id": source_type_id,
                        "target_id": target_id,
                        "target_name": target_name,
                        "target_type": target_type,
                        "target_type_id": target_type_id,
                        "edge_id": edge_id,
                        "edge_type": edge_type,
                        "edge_type_id": edge_type_id,
                        "edge_name": edge_name,
                        "direction": direction
                        })
    return results


def simple_path(kg_name, space_name, source, target, filter_event=True):
    blank_dict = {"attributes": [], "relations": []}
    G, nodes_data, edges_data, all_edges = read_graph_data(space_name, kg_name, blank_dict, direction=True,
                                                           edge_function="avg", filter_event=filter_event)
    try:
        # sp = nx.algorithms.shortest_simple_paths(G, source=source, target=target)
        sp = nx.algorithms.all_simple_paths(G, source=source, target=target)
    except nx.NetworkXNoPath as e:
        raise e
    except nx.NodeNotFound as e:
        raise e
    dicts = dict(enumerate(sp))
    result = list()
    for path in dicts.values():
        for i in range(len(path)):
            j = i + 1
            if j >= len(path):
                break
            source_id = path[i]
            source_name = nodes_data[source_id]['name']
            source_type = nodes_data[source_id]['node_type']
            source_type_id = nodes_data[source_id]['node_type_id']
            target_id = path[j]
            target_name = nodes_data[target_id]['name']
            target_type = nodes_data[target_id]['node_type']
            target_type_id = nodes_data[target_id]['node_type_id']
            key = source_id + ',' + target_id
            dict_list = all_edges[key]

            for k in dict_list:
                edge = list(list(k.items())[0])
                edge_id = edge[0]
                edge_type = edges_data[edge_id]['attributes']['edgeType']
                edge_type_id = edges_data[edge_id]['edge_type_id']
                edge_name = edges_data[edge_id]['name']
                direction = None if 'direction' not in edges_data[edge_id]['attributes'] else \
                    edges_data[edge_id]['attributes']['direction']

                result.append({"source_id": source_id,
                               "source_name": source_name,
                               "source_type": source_type,
                               "source_type_id": source_type_id,
                               "target_id": target_id,
                               "target_name": target_name,
                               "target_type": target_type,
                               "target_type_id": target_type_id,
                               "edge_id": edge_id,
                               "edge_type": edge_type,
                               "edge_type_id": edge_type_id,
                               "edge_name": edge_name,
                               "direction": direction
                               })
    li = [dict(t) for t in set([tuple(d.items()) for d in result])]
    return li


def graph_traversal(kg_name, space_name, params, source, depth_limit=None, method="dfs"):
    G, nodes_data, edges_data, _ = read_graph_data(space_name, kg_name, params["graph_rules"], direction=True,
                                                   edge_function="avg")
    if method == 'bfs':
        r = nx.algorithms.traversal.bfs_edges(G, source=source, depth_limit=depth_limit)
    else:
        r = nx.algorithms.traversal.dfs_edges(G, source=source, depth_limit=depth_limit)
    result = []
    for entity_set in r:
        result.append(list(entity_set))
    result = dict(enumerate(result))
    return result


if __name__ == '__main__':
    with open("../temp/pagerank_data_params.json", "r", encoding="utf-8") as f:
        p = json.load(f)
    # p = {"graph_rules":{"attributes":[],"relations":[]}}
    # space_name = "484412322720555008"
    # shortest_path(kg_name="480318500696793088", space_name="480318500696793088", source='480331299837747200',
    #             target='480331901179305984', params=p)
    simple_path(kg_name="480318500696793088", space_name="480318500696793088", source='480331299837747200',
                target='480331901179305984')
    # '480372882196963328,480330517855903744'
    # '480373745535721472,480372882196963328'
    # '480331299837747200,480331901179305984'
