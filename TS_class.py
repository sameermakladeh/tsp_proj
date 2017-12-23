'''definition of Travelling salesman problem Class'''
import numpy as np
import math


class Tsp():

    def __init__(self, x_co, y_co, method):
        self.x_co = x_co
        self.y_co = y_co
        self.method = method
        self.p = [self.x_co, self.y_co] #save as a point in 2D but not sure its working yet

    def dist_matrix(self):
        # build distance matrix based on the type of the tsp that is given, using the coordinates
        dist_matrix = np.zeros((len(self.x_co), len(self.y_co)))
        if self.method == 'manhattan':
            # run on all the matrix cells and in each one put the distance between 2 points (x1,y1)(x2,y2)
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
        # get a random first solution using permutations
        generated_sol = np.random.permutation(len(self.p[0]))
        return generated_sol

    def generate_neighbour(self, tsp_sol, choice):
        # generate a neighbouring solution to the current solution based on the method of search
        new_tsp_sol = list(tsp_sol)  # remember: python uses namespaces and not variables, so create a copy here!
        if choice == "swap":
            while True:
                # random 2 integers from the solution list and swap their places
                n1 = np.random.random_integers(0, len(new_tsp_sol)-1)
                n2 = np.random.random_integers(0, len(new_tsp_sol)-1)
                if n1 != n2:
                    break
            new_tsp_sol[n1], new_tsp_sol[n2] = new_tsp_sol[n2], new_tsp_sol[n1]
        return new_tsp_sol

    def solution_value(self, tsp_sol):
        # compute a solutions value using the distance matrix
        value = 0
        matrix = self.dist_matrix()
        for i in range(len(tsp_sol)):
            value = value + matrix[tsp_sol[i-1], tsp_sol[i]]
        return value
