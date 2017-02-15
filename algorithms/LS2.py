#!/usr/bin/env python
import networkx as nx
import math
import random
import utils
import time


def prob(next_size, current_size, temp):
    delta = (next_size - current_size)/(current_size//100)
    if delta <= 0:
        return 1
    else:
        return math.exp(-delta/temp)

def move_4opt(path):
    num = len(path)  # get the number of nodes in the initial solution
    seed = random.randint(0, 1000)
    random.seed(seed)
    search_space = num*10     #todo:ppt: the search space
    i = 1
    while i <= search_space:
        vertex = sorted(random.sample(path, 4))
        a, c, e, g = vertex[0], vertex[1], vertex[2], vertex[3]
        b, d, f, h = a + 1, c + 1, e + 1, g + 1
        if g == num - 1:
            h = 0
        if c - a >= 2 & e - c >= 2 & g - e >=2:
            copy_path = path[:]
            copy_path[b:d], copy_path[d:f], copy_path[f:h] = reversed(path[b:d]), reversed(path[d:f]),reversed(path[f:h])
            yield copy_path    #todo:ppt: we chose best improvement

def move_operation(path):
    num = len(path)  # get the number of nodes in the initial solution
    seed = random.randint(0, 1000)
    random.seed(seed)
    search_space = num * 10
    i = 1
    while i <= search_space:
        vertex = sorted(random.sample(path, 3))
        a, c, e = vertex[0], vertex[1], vertex[2]
        if c-a >= 2 & e-c >= 2:
            b, d, f = a+1, c+1, e+1
            copy_path = path[:]
            copy_path[b:d] = reversed(path[b:d])
            copy_path[d:f] = reversed(path[d:f])
            yield copy_path
        i += 1


def cooling_procedure(temp, para):
    while True:
        temp *= para
        yield temp
        if temp == 0:
            break


def LS2(G, cutoff, seed, temp, para):
    start = time.clock()
    random.seed(seed)
    path = G.nodes()
    best_result = []
    random.shuffle(path)
    current_seq = path
    current_path = utils.get_pathgraph(G, current_seq)
    current_size = current_path.size(weight='distance')
    for temperature in cooling_procedure(temp, para):
        for j in move_operation(current_seq):
            next_path = utils.get_pathgraph(G, j)
            next_size = next_path.size(weight='distance')  # calculate the length of potential path
            # get the cost of potential solutions
            p = prob(next_size, current_size, temperature)
            if p == 1:
                best_result.append([current_seq, current_size, temperature])
            if p > random.random():
                current_seq = j
                current_size = next_size
                break
        running_time = (time.clock()-start)
        if running_time >= cutoff:
            break
    best_path, best_weight, current_temp = best_result[0]
    for result in best_result[1:]:
        if result[1] < best_weight:
            best_path, best_weight, current_temp = result

    """
        for j in move_4opt(best_path):
        next_path = utils.get_pathgraph(G, j)
        next_size = next_path.size(weight='distance')  # calculate the length of potential path
        # get the cost of potential solutions
        if next_size < best_weight:
            # find better solutions
            best_weight = next_size
            best_path = j
    """

    return best_path, best_weight, current_temp, running_time

if __name__ == '__main__':
    print('Run the main.py file')
