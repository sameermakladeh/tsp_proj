'''Give a problem and it will solve it'''

import TS_class
from SA_alg import solve_sa
import pandas
import timeit
import numpy as np


# TODO - reorganize Main() file with proper names and calls for class/function

# get all the TSP problem from an excel file
df = pandas.read_excel('tsp.xlsx')
col_names = df.columns
col_data = df.values

# make an instance of the TSP
test_p = TS_class.Tsp(col_data[:, 0], col_data[:, 1], 'manhattan')
test_p2 = TS_class.Tsp(col_data[:, 0], col_data[:, 1], 'pure')

# generate a starting random solution for TSP
z1 = test_p2.dist_matrix()
start_time = timeit.default_timer()
z = test_p.generate_solution()

# using the starting solution generate neighbours and accept based on algorithm criteria
max_temperature = 100
min_temperature = 10
alpha = 0.8
par = [max_temperature, min_temperature, alpha]

best_solution = solve_sa(test_p, z, par[0], par[1], par[2])  # probably too bad of parameters
end_time = timeit.default_timer()

print("best sol:", best_solution, test_p.solution_value(best_solution))
print('time (sec) = ', end_time - start_time)


# TODO - remove when reorganizing

'''v_z = test_p.solution_value(z)
x = test_p.generate_neighbour(z,"swap")
w = test_p.generate_neighbour(z, "swap")
t = test_p.generate_neighbour(x, "swap")
v_x = test_p.solution_value(x)
print("z",z,v_z)
print("w",w)
print("x",x, v_x)
print("t",t)'''






