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
    print("bench is:", bench_2)

    print("best sol:", best_solution, best_solution[1])
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
        sol_i += 1

    return solution_info

