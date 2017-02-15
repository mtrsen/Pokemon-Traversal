#!/usr/bin/env python
import networkx as nx
import numpy as np
import time
import utils

best_cost = np.inf
best_solution = []
time_limit = 0


def check_cost(G, partial_solution, partial_cost):
    global best_cost
    global best_solution
    global time_limit
    if time.clock() > time_limit:
        return None, -1, -1

    if len(partial_solution) == G.number_of_nodes():
        # we have a path with all nodes but a cycle
        partial_solution.append(partial_solution[0])
        partial_cost += G[partial_solution[-2]][partial_solution[-1]]['distance']
        if partial_cost < best_cost:
            return True, partial_solution, partial_cost
        else:
            return False, -1, -1
    else:
        for node in G.nodes():
            if node not in partial_solution:
                potential_solution = partial_solution.copy()
                potential_solution.append(node)
                potential_cost = partial_cost + G[partial_solution[-1]][node]['distance']
                if potential_cost < best_cost:
                    result, new_solution, new_cost = check_cost(G, potential_solution, potential_cost)
                    if result:
                        best_cost = new_cost
                        best_solution = new_solution

        return None, -1, -1


def branch_and_bound_brute_force(G, cutoff, seed):
    """
    Branch and bound
    :param G: nx.Graph object with the nodes and appropriate weights
    :param cutoff: cutoff time for the algorithm
    :param seed: random seed
    :return: sequence to traverse the nodes
    """
    global best_cost
    global best_solution
    global time_limit

    num_nodes = G.number_of_nodes()
    time_limit = time.clock() + cutoff
    running_time = 0
    # initialize cost matrix
    cost_matrix = np.empty((num_nodes, num_nodes))
    cost_matrix[:] = np.inf
    for edge in G.edges(data=True):
        cost_matrix[edge[0], edge[1]] = edge[2]['distance']
        cost_matrix[edge[1], edge[0]] = edge[2]['distance']
    # compute initial lower bound
    lower_bound_exit_indices = np.argmin(cost_matrix, axis=1).reshape(num_nodes, -1)
    lower_bound_exit = np.min(cost_matrix, axis=1).reshape(num_nodes, -1)  # minimum costs across rows
    cost_matrix -= lower_bound_exit
    lower_bound_enter_indices = np.argmin(cost_matrix, axis=0)
    lower_bound_enter = np.min(cost_matrix, axis=0).reshape(-1, num_nodes)  # minimum costs across columns
    cost_matrix -= lower_bound_enter
    lower_bound = lower_bound_exit.sum() + lower_bound_enter.sum()

    # set initial best solution as path from 0 to num_nodes in order of indices
    best_solution = [x for x in range(0, num_nodes)]
    best_solution.append(0)
    best_pathgraph = utils.get_pathgraph(G, best_solution)
    best_cost = best_pathgraph.size(weight='distance')

    # without loss of generality we set starting point to node 0
    current_path = [0]
    current_cost = 0

    check_cost(G, current_path, current_cost)
    running_time = time.clock() - time_limit + cutoff
    return best_solution, best_cost, running_time

if __name__ == '__main__':
    print('Run the main.py file')
