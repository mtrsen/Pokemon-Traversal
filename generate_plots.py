import numpy as np
import matplotlib.pyplot as plt
import os
import math


optimum_sols = {
    'SanFrancisco': 810196,
    'NYC': 1555060,
    'Roanoke': 655454,
    'Atlanta': 2003763,
    'Champaign': 52643,
    'Cincinnati': 277952,
    'Philadelphia': 1395981,
    'UKansasState': 62962,
    'Toronto': 1176151,
    'UMissouri': 132709,
    'Boston': 893536,
    'Denver': 100431,
}

tour_lens = {
    'SanFrancisco': 99,
    'NYC': 68,
    'Roanoke': 230,
    'Atlanta': 20,
    'Champaign': 55,
    'Cincinnati': 10,
    'Philadelphia': 30,
    'UKansasState': 10,
    'Toronto': 109,
    'UMissouri': 106,
    'Boston': 40,
    'Denver': 83,
}


def generate_bnb(dirname):
    sizes = []
    qualities = []
    files = os.listdir(dirname)
    for file in files:
        instance, algorithm, rest = file.strip().split('_')
        cutoff, extension = rest.split('.')
        if extension == 'sol' and algorithm == 'BnB':
            f = open(os.path.join(dirname, file), 'r')
            sol = float(f.readline())
            qualities.append(sol/float(optimum_sols[instance]))
            sizes.append(tour_lens[instance])
    return sizes, qualities


def generate_qrtd(dirname, instance_name, algorithm_name, quality, step_size=1, max_cutoff=0):
    quality += 1
    scale = 1
    if step_size != 1:
        scale = 1.0/step_size
    run_lengths = np.zeros([1, max_cutoff])
    total_runs = 0
    files = os.listdir(dirname)
    for file in files:
        instance, algorithm, cutoff, rest = file.strip().split('_')
        seed, extension = rest.split('.')
        if extension == 'trace' and algorithm == algorithm_name and instance == instance_name:
            print(instance)
            total_runs += 1
            cutoff = int(cutoff) * scale
            if cutoff > max_cutoff:
                # run_lengths array is not long enough - so expand it
                run_lengths = np.pad(run_lengths, ((0, 0), (0, math.ceil(cutoff-max_cutoff))), mode='constant',
                                     constant_values=0)
                max_cutoff = run_lengths.shape[1]
            f = open(os.path.join(dirname, file), 'r')
            for line in f.readlines():
                run_time, sol = line.split(' ')
                run_time = float(run_time)
                time_axis = math.floor(run_time)
                sol_quality = float(sol) / float(optimum_sols[instance])
                if sol_quality < quality:
                    for time in range(math.ceil(time_axis*scale), max_cutoff):
                        run_lengths[0, time] += 1
                    break
    run_lengths /= total_runs
    return run_lengths, max_cutoff


def generate_sqd(dirname, instance_name, algorithm_name, time, step_size=1, quality_cutoff=2.5):
    scale = 1
    if step_size != 1:
        scale = 1.0/step_size
    scaled_cutoff = math.ceil(quality_cutoff * scale)
    run_lengths = np.zeros([1, scaled_cutoff])
    total_runs = 0
    files = os.listdir(dirname)
    for file in files:
        instance, algorithm, cutoff, rest = file.strip().split('_')
        seed, extension = rest.split('.')
        if extension == 'trace' and algorithm == algorithm_name and instance == instance_name:
            total_runs += 1
            f = open(os.path.join(dirname, file), 'r')
            prev_run_time = 0
            prev_sol_quality = quality_cutoff
            for line in f.readlines():
                run_time, sol = line.split(' ')
                run_time = float(run_time)
                sol_quality = float(sol) / float(optimum_sols[instance]) - 1
                if run_time > time and prev_run_time <= time:
                    for quality in range(math.ceil(prev_sol_quality*scale), scaled_cutoff):
                        run_lengths[0, quality] += 1
                    break
                prev_run_time = run_time
                prev_sol_quality = sol_quality
    run_lengths /= total_runs
    return run_lengths, scaled_cutoff


def main_bnb():
    bnb_sizes, bnb_qualities = generate_bnb('../tsp_all/solutions/')
    print(bnb_sizes)
    print(bnb_qualities)
    bnb_sizes = np.array(bnb_sizes)
    bnb_qualities = np.array(bnb_qualities)

    sort_indices = np.argsort(bnb_sizes)
    plt.xlabel('Tour length')
    plt.ylabel('Quality of solution (after 20 minutes)')
    plt.title('Fixed cutoff solution quality vs tour length - Branch and Bound')
    plt.plot(bnb_sizes[sort_indices], bnb_qualities[sort_indices], 'bo-')
    plt.grid()
    plt.show()
    print(bnb_sizes[sort_indices], bnb_qualities[sort_indices])


def main_qrtd2():
    ls_type = 2
    location = './output/LS2'
    algo = 'LS2'
    quality = 0.8
    step_size = 1
    run_lengths, max_cutoff = generate_qrtd(location, 'Toronto', algo, quality, step_size)
    start = 200
    print(run_lengths)
    print(max_cutoff)

    #qualities = [0.15, 0.18, 0.4, 1]
    qualities = [0.1, 0.18, 0.4, 1.0]
    #qualities = [x/10 for x in range(1, 10, 3)]
    x = [x*step_size for x in range(0, max_cutoff)]
    x = x[start:]
    plt.xlabel('Time (in seconds)')
    plt.ylabel('P(solve)')
    plt.annotate('Max cutoff = {} seconds'.format(max_cutoff), xy=[0.3, 0.5])
    plt.title('QRTD Plot for SA--Roanoke')
    plt.legend()
    for quality in qualities:
        run_lengths, max_cutoff = generate_qrtd(location, 'Toronto', algo, quality, step_size)
        plt.plot(x, run_lengths[0][start:])
    plt.legend(['quality = {}%'.format(int(x*100)) for x in qualities], loc='upper left')
    plt.grid()
    plt.show()


def main_qrtd1():
    ls_type = 1
    location = './output/LS1_qrtd'
    algo = 'LS1'
    quality = 0.8
    step_size = 1
    run_lengths, max_cutoff = generate_qrtd(location, 'Roanoke', algo, quality, step_size)
    start = 200
    print(run_lengths)
    print(max_cutoff)

    qualities = [0.2,0.4,0.6,0.8,1]
    #qualities = [0.1, 0.18, 0.4, 1.0]
    #qualities = [x/10 for x in range(1, 10, 3)]
    x = [x*step_size for x in range(0, max_cutoff)]
    x = x[start:]
    plt.xlabel('Time (in seconds)')
    plt.ylabel('P(solve)')
    plt.title('QRTD Plot for HC--Roanoke')
    plt.legend()
    for quality in qualities:
        run_lengths, max_cutoff = generate_qrtd(location, 'Roanoke', algo, quality, step_size)
        plt.plot(x, run_lengths[0][start:])
    plt.legend(['quality = {}%'.format(int(x*100)) for x in qualities], loc='upper left')
    plt.grid()
    plt.show()


def main_sqd2():
    ls_type = 2
    location = './output/LS2'
    algo = 'LS2'
    instance_name = 'Roanoke'
    time_limit = 600
    step_size = 0.1
    quality_cutoff = 1.1
    run_lengths, qc = generate_sqd(location, instance_name, algo, time_limit, step_size, quality_cutoff)
    start = 0
    print(run_lengths)
    print(qc)

    time_limits = [250, 300, 400, 500]
    #qualities = [0.1, 0.18, 0.4, 1.0]
    #qualities = [x/10 for x in range(1, 10, 3)]
    x = [x*step_size for x in range(0, qc)]
    x = x[start:]
    plt.xlabel('Solution quality')
    plt.ylabel('Fraction of runs')
    # plt.annotate('Max cutoff = {} seconds'.format(quality_cutoff), xy=[0.3, 0.5])
    plt.title('SQD Plot for Local search {} of different time limits'.format(ls_type))
    plt.legend()
    for time_limit in time_limits:
        run_lengths, qc = generate_sqd(location, instance_name, algo, time_limit, step_size, quality_cutoff)
        plt.plot(x, run_lengths[0][start:])
    plt.legend(['Time taken = {} seconds'.format(x) for x in time_limits], loc='upper left')
    plt.grid()
    plt.show()

def main_sqd1():
    ls_type = 1
    location = './output/LS1_qrtd'
    algo = 'LS1'
    instance_name = 'Toronto'
    time_limit = 600
    step_size = 0.1
    quality_cutoff = 3.0
    run_lengths, qc = generate_sqd(location, instance_name, algo, time_limit, step_size, quality_cutoff)
    start = 0
    print(run_lengths)
    print(qc)

    time_limits = [100, 200, 300, 400]
    #qualities = [0.1, 0.18, 0.4, 1.0]
    #qualities = [x/10 for x in range(1, 10, 3)]
    x = [x*step_size for x in range(0, qc)]
    x = x[start:]
    plt.xlabel('Solution quality')
    plt.ylabel('Fraction of runs')
    # plt.annotate('Max cutoff = {} seconds'.format(quality_cutoff), xy=[0.3, 0.5])
    plt.title('SQD Plot for Local search {} of different time limits'.format(ls_type))
    plt.legend()
    for time_limit in time_limits:
        run_lengths, qc = generate_sqd(location, instance_name, algo, time_limit, step_size, quality_cutoff)
        plt.plot(x, run_lengths[0][start:])
    plt.legend(['Time taken = {} seconds'.format(x) for x in time_limits], loc='upper left')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    #main_bnb()
    #main_qrtd1()
    #main_qrtd2()
    #main_sqd1()
    main_sqd2()
    #main_sqd()

