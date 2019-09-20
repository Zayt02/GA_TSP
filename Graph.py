import numpy as np
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, file: str):
        # self.time = 0
        self.number_of_nodes = None
        self.coords = None  # coordinate
        self.distance_matrix = None
        self._initialize(file)
        self.file = file

    def _initialize(self, file: str):
        f = open(file)
        self.number_of_nodes = int(f.readline().split()[0])
        coords = np.array([[0, 0] for _ in range(self.number_of_nodes)])
        distance_matrix = np.zeros((self.number_of_nodes, self.number_of_nodes))

        for i in range(self.number_of_nodes):
            coords[i, 0], coords[i, 1] = [float(x) for x in f.readline().split()][1:] # x, y

        self.coords = np.array(coords)
        # print(self.coords)

        fn = lambda pos1, pos2: np.sqrt(sum(t**2 for t in (pos1 - pos2)))
        for i in range(self.number_of_nodes):
            for j in range(i+1, self.number_of_nodes):
                distance_matrix[i, j] = fn(self.coords[i], self.coords[j])
                distance_matrix[j, i] = distance_matrix[i, j]
        self.distance_matrix = distance_matrix
        # print(self.distance_matrix)

    def get_distance(self, node1: int, node2: int):
        return self.distance_matrix[node1, node2]

    def show(self, route):
        x = [self.coords[route[i], 0] for i in range(len(route))]
        x.append(self.coords[route[0], 0])
        y = [self.coords[route[i], 1] for i in range(len(route))]
        y.append(self.coords[route[0], 1])
        fig = plt.figure()
        plt.plot(x, y)
        plt.plot(x, y, 'ro')
        plt.show()
        plt.savefig("result/result_" + self.file[:-4])
