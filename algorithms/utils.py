#!/usr/bin/env python
import networkx as nx
import numpy as np


def load_graph(filename, verbose=True):
    G = None    # empty graph
    n = 0   # number of nodes
    file_handle = open(filename, 'r')
    # read the initial 5 lines with info on dataset
    for i in range(0, 5):
        line = file_handle.readline()
        if i == 2:
            # read the number of nodes
            n = int(line.strip().split(' ')[-1])
        if verbose:
            print(line)
    G = nx.complete_graph(n)
    for line in file_handle.readlines()[:n]:
        node_id, x, y = line.strip().split(' ')
        node_id = int(node_id) - 1  # node id is indexed starting from 1 in .tsp file but nx.Graph indexes from 0
        G.node[node_id]['x'] = float(x)
        G.node[node_id]['y'] = float(y)
        if verbose:
            print(line)
    # fill the edges with EUC2D weights
    for u, v, d in G.edges(data=True):
        d['weight'] = int(np.sqrt((G.node[v]['x'] - G.node[u]['x'])**2 + (G.node[v]['y'] - G.node[u]['y'])**2)+0.5)
        d['distance'] = d['weight']
        if verbose:
            print("Set weight/distance between nodes(nx indexing format) {} and {} = {}".format(u, v, d['weight']))
    return G


def get_pathgraph(G, path):
    """
    :param G: main graph structure with all edges and nodes data
    :param path: list of nodes representing a sequence of edges
    :return: subgraph like structure with only the path edges and attributes from G
    """
    nlist = list(path)
    edges = zip(nlist, nlist[1:] + [nlist[0]])        #todo: change this back to the original
    H = nx.Graph()
    H.add_nodes_from(G.nodes(data=True))
    for edge in edges:
        H.add_edge(edge[0], edge[1], G.edge[edge[0]][edge[1]])
    return H


def get_elitelist(G, l, i, n):
    """
    an elite list contains the indices of the nearest nodes to a specific node in terms of Euclidean distance
    :param G: main graph structure will all edges and nodes data
    :param l: the size of the vertex set
    :param i: a node for which we want to find the elite list
    :param n: the size of the elite list
    :return: an elite list of size n of the node i.
    """
    neighbor_list = []
    for j in range(l):
        if j == i:
            neighbor_list.append(9999999)
        elif i > j:
            neighbor_list.append(G.edge[j][i]['distance'])
        else:
            neighbor_list.append(G.edge[i][j]['distance'])
    return tuple(sorted(range(len(neighbor_list)), key=lambda k: neighbor_list[k])[:n])



def save_results(G, solution):
    """
    :param G: original graph data
    :param solution: list containing the best tour nodes
    :return: string to be written to the save file
    """
    result_str = ""
    cost = 0
    edges = zip(solution, solution[1:]+[solution[0]])           #todo: change this back to the original
    for edge in edges:
        edge_cost = int(G.edge[edge[0]][edge[1]]['distance'])
        result_str += "{} {} {}\n".format(int(edge[0]), int(edge[1]), edge_cost)
        cost += edge_cost
    begin_str = str(int(cost)) + '\n'
    return begin_str + result_str.strip('\n')

if __name__ == '__main__':
    print('Run the main.py file')