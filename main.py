from Graph import *
from GA import GA


def main(file: str):
    graph = Graph(file)
    alg = GA(graph)
    best_route = alg.loop()
    print(best_route.gen)
    print(-best_route.fitness)
    graph.show(best_route.gen)


if __name__ == '__main__':
    main("wi29.txt")
