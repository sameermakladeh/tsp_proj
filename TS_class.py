'''definition of Travelling salesman problem Class'''
import numpy as np

class Tsp():

    def __init__(self,x_co,y_co,method):
        self.x_co = x_co
        self.y_co = y_co
        self.method = method

    def dist_matrix(self):
        if self.method == 'manhattan':
            dist_matrix = np.zeros((len(self.x_co),len(self.y_co)))
            for i in range(dist_matrix.shape[0]):
                for j in range(dist_matrix.shape[1]):
                    dist_matrix[i][j] = np.linalg.norm(self.x_co[i] - self.y_co[j])
        return dist_matrix

