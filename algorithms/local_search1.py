#!/usr/bin/env python
import random
import utils
import time

#perturbation

def move_old(path):
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
            copy_path[b:d],copy_path[d:f] = reversed(path[b:d]),reversed(path[d:f])
            yield copy_path
        i += 1

def move_3opt(path, elite_list):
    num = len(path)  # get the number of nodes in the initial solution
    seed = random.randint(0, 1000)
    random.seed(seed)
    search_space = num * 10
    i = 1

    while i <= search_space:
        vertex = sorted(random.sample(path, 3))
        a, c, e = vertex[0], vertex[1], vertex[2]
        b, d, f= a + 1, c + 1, e + 1
        if e == num-1:
            f = 0
        if c - a >= 2 & e - c >= 2 & (a in elite_list[c]) & (b in elite_list[e]) & (d in elite_list[f]):
            copy_path = path[:]
            copy_path[b:d],copy_path[d:f] = reversed(path[b:d]),reversed(path[d:f])
            yield copy_path
        i += 1

def move_4opt(path, elite_list):
    num = len(path)  # get the number of nodes in the initial solution
    seed = random.randint(0, 1000)
    print("seed = {}".format(seed))
    random.seed(seed)
    search_space = num*5     #todo:ppt: the search space
    i = 1
    while i <= search_space:
        print ("{}th time inside while ".format(i))
        vertex = sorted(random.sample(path, 4))
        a, c, e, g = vertex[0], vertex[1], vertex[2], vertex[3]
        b, d, f, h = a + 1, c + 1, e + 1, g + 1
        if g == num - 1:
            h = 0
        if c - a >= 2 & e - c >= 2 & g - e >=2 & (c in elite_list[a]) & (b in elite_list[e]) & (d in elite_list[g]) & (f in elite_list[h]):
            print ("++++++++++++++")
            copy_path = path[:]
            copy_path[b:d], copy_path[d:f], copy_path[f:h] = reversed(path[b:d]), reversed(path[d:f]),reversed(path[f:h])
            yield copy_path    #todo:ppt: we chose best improvement
        i += 1

def local_search1(G, cutoff, seed):
    # initialize seed
    start = time.clock()
    random.seed(seed)
    path = G.nodes()  # initial path of nodes
    max_global_iterations = 1000
    i = 0
    global_results = []
    running_time = 0

    elite_list = []
    elitelist_size = int(len(path)//1.1)     #todo:ppt: elite list size
    for k in range(len(path)):
        elite_list.append(utils.get_elitelist(G, len(path), k, elitelist_size))

    while i <= max_global_iterations:
        i += 1
        random.shuffle(path)  # generate random permutation of path
        result_path = path
        pathgraph = utils.get_pathgraph(G, path)
        current = pathgraph.size(weight='distance')  # find the length of initial solution
        iteration = 1
        local_iteration = len(path)*5
        while iteration <= local_iteration:
            iteration += 1
            move = False
            # initialize move operation
            num_improvement = 0
            for j in move_4opt(result_path,elite_list):
                result = utils.get_pathgraph(G, j)
                next_size = result.size(weight='distance')  # calculate the length of potential path
            # get the cost of potential solutions
                if next_size < current:
                    # find better solutions
                    num_improvement+=1
                    print("find improvement {}th!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!".format(num_improvement))
                    current = next_size
                    result_path = j
                    move = True
            if not move:
                break
            # break the loop if there is no move
        global_results.append([result_path, current, iteration, i])
        running_time = (time.clock() - start)
        if running_time >= cutoff:
            break
    best_path, best_size, best_iterations, best_i = global_results[0]
    for result in global_results[1:]:
        if result[1] < best_size:
            best_path, best_size, best_iterations, best_i = result

    return best_path, best_size, best_iterations, best_i, running_time


if __name__ == '__main__':
    print('Run the main.py file')