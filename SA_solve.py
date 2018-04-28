'''Give a problem and it will solve it'''

import TS_class
from SA_alg import solve_sa
from SA_alg import calc_interval
import pandas
import timeit
# import SA_GUI
import numpy as np



# TODO - reorganize Main() file with proper names and calls for class/function

optimm = 27603 # based on the western Sahara 29 cities

def solve(data, parameters):

    ''' make an instance of the TSP '''
    xdata, ydata, dtype = data[:, 0], data[:, 1], 'pure'
    test_p = TS_class.Tsp(xdata, ydata, dtype)

    # test_p2 = TS_class.Tsp(col_data[:, 0], col_data[:, 1], 'pure')

    ''' generate a starting random solution for TSP '''
    # z1 = test_p2.dist_matrix()

    start_time = timeit.default_timer()
    z = test_p.generate_solution()

    '''  using the starting solution generate neighbours and accept based on algorithm criteria '''

    best_solution = solve_sa(test_p, z, parameters[0], parameters[1], parameters[2], parameters[3])

    end_time = timeit.default_timer()

    #bench_2 = optimm/best_solution[1]
    #print("bench is:", bench_2)

    print("best sol:", best_solution[0], best_solution[1], best_solution[2])
    print('time (sec) = ', end_time - start_time)

    return best_solution, end_time


def find_outline(data, parameters):

    ''' build the confidence interval for which the decision will be based on what is an out layer point '''
    w, h, history_num = 3, 38, 100      # TODO: Get a data set in the size of the grid
    dtype = 'pure'
    history = [[None] * w for i in range(history_num)]
    j, hist = 0, 0
    used_hub = []
    inter_data = []
    while j < history_num:
        history_data = np.zeros((37, 2))       # TODO: Save reduced problem data
        ''' sample a random hub to take out and calculate solution without'''
        ran_num = np.random.randint(0, 38)     # TODO: Get a data set in the size of the grid
        used_hub = ran_hub = data[ran_num][:]
        i = 0
        for d in data:
            if not (d[0] == ran_hub[0] and d[1] == ran_hub[1]):
                history_data[i][0] = d[0]
                history_data[i][1] = d[1]
                i += 1
        history_xdata = history_data[:, 0]
        history_ydata = history_data[:, 1]

        history_outline = TS_class.Tsp(history_xdata, history_ydata, dtype)

        ''' generate a starting random solution for TSP '''
        start_time = timeit.default_timer()
        history_out = history_outline.generate_solution()

        '''  using the starting solution generate neighbours and accept based on algorithm criteria '''
        best_solution_history_out = solve_sa(history_outline, history_out,
                                                 parameters[0], parameters[1], parameters[2], parameters[3])
        end_time = timeit.default_timer()

        history[hist] = [(used_hub[0], used_hub[1]),  best_solution_history_out[1], best_solution_history_out[2]]
        inter_data.append(history[hist][1])
        hist += 1
        j += 1
    history_interval = calc_interval(inter_data)  # calculate the confidence interval of the history solutions

    ''' For each hub make an instance of the TSP without it and check if its an outlier point '''
    solution_info = [[None] * w for i in range(h)]
    sol_i = 0
    for hub in data:
        new_data = np.zeros((37, 2))       # TODO: Save reduced problem data
        i = 0
        for x in data:
            if not (x[0] == hub[0] and x[1] == hub[1]):
                new_data[i][0] = x[0]
                new_data[i][1] = x[1]
                i += 1
        new_xdata = new_data[:, 0]
        new_ydata = new_data[:, 1]

        test_outline = TS_class.Tsp(new_xdata, new_ydata, dtype)

        ''' generate a starting random solution for TSP '''
        start_time = timeit.default_timer()
        out = test_outline.generate_solution()

        '''  using the starting solution generate neighbours and accept based on algorithm criteria '''
        best_solution_out = solve_sa(test_outline, out, parameters[0], parameters[1], parameters[2], parameters[3])
        end_time = timeit.default_timer()

        if best_solution_out[1] > history_interval[1]:
            bench = "Outlier!"
        else:
            bench = "meh, normal..."

        print("bench is:", bench)

        solution_info[sol_i] = [(hub[0], hub[1]),  best_solution_out[1], history_interval, bench]
        print("remove:", solution_info[sol_i][0], "value:", best_solution_out[1])
        print('time (sec) = ', end_time - start_time)
        sol_i += 1

    return solution_info


def ml_solve(data, parameters):

    ''' Get a problem and initial parameters then learn and try to suggest a better parameters to use '''

    xdata, ydata, dtype = data[:, 0], data[:, 1], 'pure'
    test_ml = TS_class.Tsp(xdata, ydata, dtype)

    ''' generate a starting random solution for TSP '''
    start_time = timeit.default_timer()
    ml = test_ml.generate_solution()

    ''' using the starting solution generate neighbours and accept based on algorithm criteria '''
    ''' instead if using the given parameters, try and find better ones with a random loop '''
    original_solution = solve_sa(test_ml, ml, parameters[0], parameters[1], parameters[2], parameters[3])
    original_pars = list(parameters)

    ''' manipulate the given parameters and get back the best ones'''
    labels = ["max temperature", "min temperature", "alpha", "loops"]
    new_parameters = list(parameters)
    top_pars = [labels, parameters, [0, 0, 0, 0]]     # make a list with size 4
    ml_gbest = tuple(original_solution)
    loops = 10

    for p in range(0, len(top_pars[0][:])):
        ''' for each parameter loop individually and check it's improvement '''
        best_par = 0
        best_bench = 1
        for num in range(1, loops):
            if top_pars[0][p] == "max temperature":
                new_par = np.random.random_integers(100, 1000)
                ml_solution = solve_sa(test_ml, ml, new_par, parameters[1], parameters[2], parameters[3])
                bench_sol = ml_solution[1] / original_solution[1]
                if bench_sol < 1 and bench_sol < best_bench:
                    ''' if it's a better solution, save it '''
                    best_par = new_par
                    best_bench = bench_sol
                    if ml_solution[1] < ml_gbest[1]:
                        ml_gbest = ml_solution

            elif top_pars[0][p] == "min temperature":
                new_par = np.random.random_integers(10, 100)
                ml_solution = solve_sa(test_ml, ml, parameters[0], new_par, parameters[2], parameters[3])
                bench_sol = ml_solution[1] / original_solution[1]
                if bench_sol < 1 and bench_sol < best_bench:
                    ''' if it's a better solution, save it '''
                    best_par = new_par
                    best_bench = bench_sol
                    if ml_solution[1] < ml_gbest [1]:
                        ml_gbest = ml_solution

            elif top_pars[0][p] == "alpha":
                while True:
                    new_par = round(np.random.rand(1)[0], 2)
                    if 0.05 < new_par < 0.9:
                        break  # this condition limits the values of alpha TODO: change if necessary
                ml_solution = solve_sa(test_ml, ml, parameters[0], parameters[1], new_par, parameters[3])
                bench_sol = ml_solution[1] / original_solution[1]
                if bench_sol < 1 and bench_sol < best_bench:
                    ''' if it's a better solution, save it '''
                    best_par = new_par
                    best_bench = bench_sol
                    if ml_solution[1] < ml_gbest [1]:
                        ml_gbest = ml_solution

            elif top_pars[0][p] == "loops":
                new_par = np.random.random_integers(10, 100)
                ml_solution = solve_sa(test_ml, ml, parameters[0], parameters[1], parameters[2], new_par)
                bench_sol = ml_solution[1] / original_solution[1]
                if bench_sol < 1 and bench_sol < best_bench:
                    ''' if it's a better solution, save it '''
                    best_par = new_par
                    best_bench = bench_sol
                    if ml_solution[1] < ml_gbest [1]:
                        ml_gbest = ml_solution

        ''' assign all the best parameters found into the array top_pars '''
        if best_par > 0:
            top_pars[1][p] = best_par
        top_pars[2][p] = best_bench

        ''' change to the new parameters and use them to calculate new solution (optimized) '''
    for ix in range(0, len(new_parameters)):
        new_parameters[ix] = top_pars[1][ix]

    ml_best = solve_sa(test_ml, ml, new_parameters[0], new_parameters[1], new_parameters[2], new_parameters[3])
    if ml_best[1] < ml_gbest[1]:
        ml_gbest = ml_best

    print("max temperature: %d" %new_parameters[0], ", min temperature: %d" %new_parameters[1],
          ", alpha: %.2f" %new_parameters[2], ", loops: %d" %new_parameters[3], "\nbest solution: ", ml_gbest[1],
          "\nbenchmarks: ", top_pars[2][:])

    print(top_pars[1][:], "\nbest solution: ", ml_gbest[1],
          "\nbenchmarks:", top_pars[2][:])

    return original_solution, original_pars, ml_gbest, new_parameters


