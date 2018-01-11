'''An algorith to solve a given TSP'''

import numpy as np
import math


def solve_sa(tsprob, current_solution, t_max, t_min, alpha, iter_n):
    ''' get a given solution for the tsp and find a better one using the algorithm '''
    v_curr = tsprob.solution_value(current_solution)
    t = t_max
    while t > t_min:
        for p in range(int(iter_n)):
            new_solution = tsprob.generate_neighbour(current_solution,"swap")
            v_new = tsprob.solution_value(new_solution)
            delta = v_new - v_curr
            ap = min(1,math.exp(-delta/t))
            # show the current solution and its value, and also the new solution and its value
            print('current sol:', current_solution, v_curr)
            print('check sol:', new_solution, v_new)
            if v_new < v_curr:  # if value is better accept, if not use metropolis criteria
                current_solution = new_solution
                v_curr = v_new
                print("accepted sol - value:", current_solution, v_curr)
            elif ap > np.random.rand(1):  # random a number to use in metropolis criteria
                current_solution = new_solution
                v_curr = v_new
                print("accepted sol - prob:", current_solution, v_curr)
        t = t*alpha
    return current_solution  # TODO - need to add the option for storing best solution found since the start of the alg.



