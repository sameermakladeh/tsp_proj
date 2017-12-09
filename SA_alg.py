'''Give a problem and it will solve it'''

import TS_class
import pandas

'''get all the TSP problem from an excel file'''
df = pandas.read_excel('tsp.xlsx')
col_names = df.columns
col_data = df.values


test_p = TS_class.Tsp(col_data[:, 0], col_data[:, 1], 'manhattan')
test_p2 = TS_class.Tsp(col_data[:, 0], col_data[:, 1], 'pure')


z = test_p2.dist_matrix()
print(z)






