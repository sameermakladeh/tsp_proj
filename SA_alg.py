'''Give a problem and it will solve it'''

import TS_class
import pandas

'''get all the TSP problem from an excel file'''
df = pandas.read_excel('tsp.xlsx')
col_names = df.columns
col_data = df.values

test_p = TS_class.Tsp([1,2,3,4],[1,2,3,4],'manhattan')
test_p2 = TS_class.Tsp([1,2,3,4],[1,2],'manhattan')

z = test_p.dist_matrix()
z2 = test_p2.dist_matrix()
print(z)
print("\n", z2)





