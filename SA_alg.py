'''Give a problem and it will solve it'''

import TS_class
import pandas
import numpy as np



'''get all the TSP problem from an excel file'''
df = pandas.read_excel('tsp.xlsx')
col_names = df.columns
col_data = df.values


test_p = TS_class.Tsp(col_data[:, 0], col_data[:, 1], 'manhattan')
test_p2 = TS_class.Tsp(col_data[:, 0], col_data[:, 1], 'pure')


z1 = test_p2.dist_matrix()
z = test_p.generate_solution()
v_z = test_p.solution_value(z)
print(z,v_z)
x = test_p.generate_neighbour(z,"swap")
v_x = test_p.solution_value(x)
print(x,v_x)






