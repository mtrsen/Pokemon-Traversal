#!/usr/bin/env python
import utils
import random
import argparse
import os
from branch_and_bound import *
from branch_and_bound_brute_force import *
from mst_approx import *
from heuristic import *
from local_search1 import *
from LS2 import *


def main():
    randseed = random.randint(0, 10000)
    parser = argparse.ArgumentParser(description='CSE 6140 Project implementation')
    parser.add_argument('-inst', '--filename', help='dataset instance')
    parser.add_argument('-alg', '--algorithm', help='algorithm type - BnB | MSTApprox | Heur | LS1 | LS2')
    parser.add_argument('-time', '--cutoff', help='cutoff time in seconds', type=int, default=100)
    parser.add_argument('-para', '--para', help='parameter for SA', type=float)
    parser.add_argument('-temp', '--temp', help='temperature for SA', type=int)
    parser.add_argument('-seed', '--seed', type=int, help='random seed', default=randseed)

    args = parser.parse_args()
    graph = utils.load_graph(args.filename)

    print("Cutoff used = {}".format(args.cutoff))
    print("Seed used = {}".format(args.seed))

    if args.algorithm == 'BnB':
        path, cost, running_time = branch_and_bound(graph, float(args.cutoff), int(args.seed))
        path2, cost2, running_time2 = branch_and_bound_brute_force(graph, float(args.cutoff), int(args.seed))
        print("Path = {}".format(path2))
        print("Distance = {}".format(cost2))
        print("BnB brute force Running time={}".format(running_time2))
    elif args.algorithm == 'MSTApprox':
        mst_approx(graph, float(args.cutoff), int(args.seed))
    elif args.algorithm == 'Heur':
        heuristic(graph, float(args.cutoff), int(args.seed))
    elif args.algorithm == 'LS1':
        path, cost, iterations, global_iterations, running_time = local_search1(graph, float(args.cutoff), int(args.seed))
        print("Num of local iterations = {}".format(iterations))
        print("Best global iteration = {}".format(global_iterations))
    elif args.algorithm == 'LS2':
        path, cost, temperature, running_time = LS2(graph, float(args.cutoff), int(args.seed), int(args.temp), float(args.para))
        print("Path = {}".format(path))
        print("Distance = {}".format(cost))
        print("Running time={}".format(running_time))
        print("temperature={}".format(temperature))
        base_filename = os.path.basename(args.filename).split('.')[0] + '_' + args.algorithm + '_' + str(args.cutoff)
    if args.algorithm != 'BnB':
        base_filename += '_' + str(args.seed)
    # write the solution file
    solution_file = os.path.join(os.path.dirname(args.filename), base_filename + '.sol')
    file_handle = open(solution_file, 'w')
    file_handle.write(utils.save_results(graph, path))
    file_handle.close()

    # write the trace file

if __name__ == "__main__":
    main()