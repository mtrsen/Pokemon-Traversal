#!/usr/bin/env python

import networkx as nx
import heapq as hq
import numpy as np
import time


def mst_approx(G, time, randseed):

    """
    mst-approx
    :param G:
    :param cutoff:
    :param seed:
    :return:

    """

    start = time.time()
    # Find the MST of G
    MST, MST_cost = find_mst(G)

    # DFS starting with root node - 0
    order = depth_first_search(MST, 0)

    # Calculate cost of the order given by the DFS
    cost, weights = cost_approx(G, order)
    end = time.time()

    time = end-start

    return cost, order, time

def cost_approx(G, order):

    """

    :param G:
    :param order:
    :return: cost of estimated MST Approx

    """
    N = len(order)

    cost = 0
    weights = []
    for i in range(0, N-1):
        node = order[i]
        node1 = order[i+1]
        weight = nx.Graph.get_edge_data(G, node, node1)
        w = weight.__getitem__('weight')
        cost = cost + w
        weights = weights + [w]

    ret = nx.Graph.get_edge_data(G, order[N-1], order[0])
    ret_w = ret.__getitem__('weight')
    cost = cost + ret_w
    weights = weights + [ret_w]

    return cost, weights


def find_mst(G):

    """
    Implementation of Prim's Algorithm
    :param G:
    :return: T, C: MST graph and MST cost
    """

    # number of nodes
    N = nx.Graph.__len__(G)

    # initialize MST graph, cost and visited nodes
    MST = nx.Graph()
    MST_cost = 0
    visited_nodes = np.zeros(N)    # array of visited nodes; 0 if unvisited
    visited_nodes[0] = 1           # add node 1
    new_node = 0
    MST.add_node(new_node)

    # initialize heap with edges to node 1
    heap = []
    add_edges = nx.Graph.edges(G, new_node, data='weight')
    for i in range(0, (N-1)):

        # hq requires - weight, node1, node2
        e = add_edges[i]
        n = (e[2], e[0], e[1])

        # add edge to the the heap
        hq.heappush(heap, n)

    # when all nodes are visited all elements of visited_nodes will = 1
    while min(visited_nodes) == 0:

        # pop smallest weight edge (and new node)
        min_w = hq.heappop(heap)
        new_weight, current_node, new_node = min_w[0], min_w[1], min_w[2]

        # check if the given node has been visited
        # if not continue if so pop next smallest weight and repeat
        if visited_nodes[new_node] == 0:
            # add the new node to the MST
            visited_nodes[new_node] = 1
            MST.add_edge(current_node, new_node, weight=new_weight)

            # update current cost of MST
            MST_cost = MST_cost + new_weight

            # add new edges; from the newly added node
            add_edges = nx.Graph.edges(G, new_node, data='weight')
            for i in range(0, (N-1)):

                # only add new edges
                # adding new_node to current_node is redundant
                # since current_node to new_node is already in the heap
                e = add_edges[i]
                # hq requires - weight, node1, node2
                n = (e[2], e[0], e[1])

                # add edge to the the heap
                hq.heappush(heap, n)

    return MST, MST_cost


def depth_first_search(MST, r):

    """
    Implementation of DFS on MST graph

    :param MST: Graph of MST
    :param r: root node
    :return: list of nodes in order to be used to estimate TSP instance
    """

    N = nx.Graph.__len__(MST)
    nodes = [i for i in range(N)]

    # create adjacency matrix
    adj = nx.to_numpy_matrix(MST)

    explored_nodes = np.zeros(N)
    ordered_explored = []

    stack = [r]
    while len(stack) > 0:
        u = stack.pop()

        if explored_nodes[u] == 0:
            explored_nodes[u] = 1
            ordered_explored = ordered_explored + [u]
            # print("order: ")
            # print(ordered_explored)

            au = adj[u]                              # uth row of the adj matrix
            au = au.getA1()                          # flatten to an array
            au_wei = list(au[au > 0])                # list of non-zero elements
            au_wei.sort(reverse=True)                # sort list of non-zero elements (large to small)

            au = list(au)
            # loop through all non-zero elements & add the adjacent nodes in order of farthest to closest
            # such that the stack has the closest nodes at the far end (search through those first)
            # ensure there are any new nodes from node u to be added
            if au_wei is not None:
                for i in range(0, len(au_wei)):

                    weight = au_wei[i]
                    # print(weight)
                    node = au.index(weight)
                    # print(node)
                    stack = stack + [node]
                    # print(stack)

    return ordered_explored


if __name__ == '__main__':
    print('Run the main.py file')
