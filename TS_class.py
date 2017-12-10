'''definition of Travelling salesman problem Class'''
import numpy as np
import math

class Tsp():

    def __init__(self, x_co, y_co, method):
        self.x_co = x_co
        self.y_co = y_co
        self.method = method
        self.p = [self.x_co, self.y_co] #save as a point in 2D but not sure

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

    def generate_solution(self):
        generated_sol = np.random.permutation(len(self.p[0]))
        return generated_sol

    def generate_neighbour(self, tsp_sol, choice):
        if choice == "swap":
            while True:
                n1 = np.int(np.floor(np.random.uniform(0, len(tsp_sol))))
                n2 = np.int(np.floor(np.random.uniform(0, len(tsp_sol))))
                if n1 != n2:
                    break
            tsp_sol[n1], tsp_sol[n2] = tsp_sol[n2], tsp_sol[n1]
        return tsp_sol

    def solution_value(self, tsp_sol):
        value = 0
        matrix = self.dist_matrix()
        for i in range(len(tsp_sol)):
            value = value + matrix[tsp_sol[i-1], tsp_sol[i]]
        return value
