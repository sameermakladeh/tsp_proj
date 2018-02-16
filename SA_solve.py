'''Give a problem and it will solve it'''

import TS_class
from SA_alg import solve_sa
import pandas
import timeit
# import SA_GUI
import numpy as np

# TODO - reorganize Main() file with proper names and calls for class/function


def solve(data, paramaters):

    ''' make an instance of the TSP '''
    xdata, ydata, dtype = data[:, 0], data[:, 1], 'manhattan'
    test_p = TS_class.Tsp(xdata, ydata, dtype)

    # test_p2 = TS_class.Tsp(col_data[:, 0], col_data[:, 1], 'pure')

    ''' generate a starting random solution for TSP '''
    # z1 = test_p2.dist_matrix()
    start_time = timeit.default_timer()
    z = test_p.generate_solution()

    '''  using the starting solution generate neighbours and accept based on algorithm criteria '''

    best_solution = solve_sa(test_p, z, paramaters[0], paramaters[1], paramaters[2], paramaters[3])

    end_time = timeit.default_timer()

    print("best sol:", best_solution, test_p.solution_value(best_solution))
    print('time (sec) = ', end_time - start_time)

    return best_solution, test_p.solution_value(best_solution), end_time






