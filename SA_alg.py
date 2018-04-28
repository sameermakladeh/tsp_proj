'''An algorith to solve a given TSP'''

import numpy as np
from math import exp as ex
import statistics as st
from scipy import stats as stat
import timeit


def calc_interval(arr):
    '''  calculates the confidence interval of all the runs made by SA to determine credibility '''
    print(arr)
    n = len(arr)
    x_mean = st.mean(arr)
    conf_interval = stat.t.interval(0.95, n-1, x_mean, stat.sem(arr))
    return conf_interval


def solve_sa(tsprob, current_solution, t_max, t_min, alpha, iter_n):
    ''' get a given solution for the tsp and find a better one using the algorithm and check if statistically valid'''
    s_time = timeit.default_timer()     # used to kill long run times
    K = 0
    exp_value = []
    g_best_sol = list(current_solution)
    v_gbest_sol = tsprob.solution_value(g_best_sol)
    while K < 50:       # TODO: Change for smaller problems
        v_curr = tsprob.solution_value(current_solution)
        loc_best_sol = list(current_solution)
        v_loc_best = tsprob.solution_value(loc_best_sol)
        t = t_max
        while t > t_min:
            for p in range(int(iter_n)):
                new_solution = tsprob.generate_neighbour(current_solution,"swap")
                v_new = tsprob.solution_value(new_solution)
                delta = v_new - v_curr
                if -delta/t > 0:
                    mp = 1
                else:
                    mp = round(ex(-(delta/t)), 2)
                ap = min(1.0, mp)
                # show the current solution and its value, and also the new solution and its value
                # print('current sol:', current_solution, v_curr)
                # print('checked sol:', new_solution, v_new)
                if v_new < v_curr:  # if value is better accept, if not use metropolis criteria
                    current_solution = new_solution
                    v_curr = v_new
                    if v_new < v_loc_best:
                        ''' if a better solution is found that the local run in the Temperature, save it '''
                        loc_best_sol = list(new_solution)
                        v_loc_best = v_new
                    if v_new < v_gbest_sol:
                        ''' if a better solution is found, globally, the the SA runs, save it '''
                        g_best_sol = list(new_solution)
                        # print(timeit.default_timer())  # For timing purposes!
                        v_gbest_sol = v_new
                        # print("GBHEST - value:", g_best_sol, v_gbest)
                    # print("accepted sol - value:", current_solution, v_curr)
                elif ap > np.random.rand(1):  # random a number to use in metropolis criteria
                    current_solution = new_solution
                    v_curr = v_new
                    # print("accepted sol - prob:", current_solution, v_curr)
            t = t*alpha
        exp_value.append(v_loc_best)
        K += 1
        if timeit.default_timer() - s_time > 600: # Limit to 600 seconds loop for long runs
            break
    interval = calc_interval(exp_value)  # calculate the confidence interval of the solutions
    return g_best_sol, v_gbest_sol,  interval  # returns best solution since the start of the alg.


