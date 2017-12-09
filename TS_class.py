'''definition of Travelling salesman problem Class'''
import numpy as np
import math

class Tsp():

    def __init__(self, x_co, y_co, method):
        self.x_co = x_co
        self.y_co = y_co
        self.method = method
        self.p = [self.x_co, self.y_co] #save as a point in 2D

    def dist_matrix(self):
        dist_matrix = np.zeros((len(self.x_co), len(self.y_co)))
        if self.method == 'manhattan':
            for i in range(dist_matrix.shape[0]):
                for j in range(dist_matrix.shape[1]):
                    dist_matrix[i][j] = abs(self.x_co[i] - self.x_co[j])+abs(self.y_co[i] - self.y_co[j])
        if self.method == 'pure':
            for i in range(dist_matrix.shape[0]):
                for j in range(dist_matrix.shape[1]):
                    dist_matrix[i][j] = math.sqrt(pow((self.x_co[i] - self.x_co[j]), 2) +
                                                  pow((self.y_co[i] - self.y_co[j]), 2))
        return dist_matrix