'''Give a problem and it will solve it'''

import TS_class
from SA_alg import solve_sa
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

    bench_2 = optimm/best_solution[1]
    #print("bench is:", bench_2)

    print("best sol:", best_solution[0], best_solution[1], best_solution[2])
    print('time (sec) = ', end_time - start_time)

    return best_solution, end_time


def find_outline(data, parameters):

    ''' For each hub make an instance of the TSP without it and check if its an outline '''

    w, h = 3, 29
    solution_info = [[None] * w for i in range(h)]
    dtype = 'pure'
    sol_i = 0
    for hub in data:
        new_data = np.zeros((28, 2))
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

        bench = optimm/best_solution_out[1]
        print("bench is:", bench)

        solution_info[sol_i] = [(hub[0], hub[1]),  best_solution_out[1], "%.2f" %bench]
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

    for p in range(0, len(top_pars[0][:])):
        ''' for each parameter loop individually and check it's improvement, then rank them '''
        best_par = 0
        best_bench = 1
        for num in range(1, 2):
            if top_pars[0][p] == "max temperature":
                new_par = np.random.random_integers(100, 1000)
                ml_solution = solve_sa(test_ml, ml, new_par, parameters[1], parameters[2], parameters[3])
                bench_sol = ml_solution[1] / original_solution[1]
                if bench_sol < 1 and bench_sol < best_bench:
                    best_par = new_par
                    best_bench = bench_sol
                    if ml_solution[1] < ml_gbest [1]:
                        ml_gbest = ml_solution

            elif top_pars[0][p] == "min temperature":
                new_par = np.random.random_integers(10, 100)
                ml_solution = solve_sa(test_ml, ml, parameters[0], new_par, parameters[2], parameters[3])
                bench_sol = ml_solution[1] / original_solution[1]
                if bench_sol < 1 and bench_sol < best_bench:
                    best_par = new_par
                    best_bench = bench_sol
                    if ml_solution[1] < ml_gbest [1]:
                        ml_gbest = ml_solution

            elif top_pars[0][p] == "alpha":
                new_par = round(np.random.rand(1)[0], 2)
                ml_solution = solve_sa(test_ml, ml, parameters[0], parameters[1], new_par, parameters[3])
                bench_sol = ml_solution[1] / original_solution[1]
                if bench_sol < 1 and bench_sol < best_bench:
                    best_par = new_par
                    best_bench = bench_sol
                    if ml_solution[1] < ml_gbest [1]:
                        ml_gbest = ml_solution

            elif top_pars[0][p] == "loops":
                new_par = np.random.random_integers(10, 200)
                ml_solution = solve_sa(test_ml, ml, parameters[0], parameters[1], parameters[2], new_par)
                bench_sol = ml_solution[1] / original_solution[1]
                if bench_sol < 1 and bench_sol < best_bench:
                    best_par = new_par
                    best_bench = bench_sol
                    if ml_solution[1] < ml_gbest [1]:
                        ml_gbest = ml_solution
        if best_par > 0:
            top_pars[1][p] = best_par
        top_pars[2][p] = best_bench

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


