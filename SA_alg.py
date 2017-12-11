'''An algorith to solve a given TSP'''

import numpy as np


def solve_sa(tsprob, current_solution):
    # get a given solution for the tsp and find a better one using the algorithm
    arg_p = np.random.rand(1)  #for now, just a random number p
    for i in range(1,10):
        # show the current solution and its value, and also the new solution and its value
        v_1 = tsprob.solution_value(current_solution)
        new_solution = tsprob.generate_neighbour(current_solution,"swap")
        v_2 = tsprob.solution_value(new_solution)
        r = np.random.rand(1)  # random a number to use in metropolis criteria
        print("current_sol:", current_solution, v_1)
        print("check:", new_solution, v_2)
        print(r, arg_p)
        # do a check on both the values and a given probability for acceptance criteria
        if v_2 < v_1 and r < arg_p:
            current_solution = new_solution
            print("accepted sol:", current_solution, tsprob.solution_value(current_solution))
    return current_solution
