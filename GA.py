import numpy as np
import copy

from collections import defaultdict
from Graph import Graph

SEED = 2
LOOP_COUNT = 600
POP_SIZE = 100
CX_PROB = 0.7
MUTATION_PROB = 0.2


class Individual:
    def __init__(self, gen):
        self.gen = gen
        self.fitness = None

    def set_fitness(self, fitness):
        self.fitness = fitness


class GA:
    def __init__(self, graph: Graph):
        np.random.seed(SEED)
        self.graph = graph
        self.number_of_nodes = self.graph.number_of_nodes # so dinh
        self.list_node = range(self.number_of_nodes) # danh sach ten cac dinh
        self.population = [Individual(self._generate_gen()) for _ in range(POP_SIZE)]
        self.cx_prob = CX_PROB # xac suat lai ghep
        self.mutation_prob = MUTATION_PROB  # xac suat dot bien
        self.loop_count = LOOP_COUNT
        self.roulette_wheel = np.array([0 for _ in range(POP_SIZE)]) # bo qua
        self.set_pop_fitness(self.population)
        # print([individual.fitness for individual in self.population])
        self.best_individual = copy.copy(np.random.choice(self.population))

    def _get_fitness(self, individual: Individual):
        fitness = 0
        for i in range(1, len(individual.gen)):
            fitness += self.graph.get_distance(individual.gen[i-1], individual.gen[i])
        fitness += self.graph.get_distance(individual.gen[-1], individual.gen[0])
        return -fitness

    def set_pop_fitness(self, pop: list):
        for individual in pop:
            individual.set_fitness(self._get_fitness(individual))

    def _generate_gen(self):
        """generate a list and sort it"""
        gen = []
        l1 = list(np.random.uniform(0, 1, self.number_of_nodes))
        l2 = sorted(l1)
        for i in l2:
            gen.append(self.list_node[l1.index(i)])

        return gen

    def _build_roulette_wheel(self):
        s = 0
        self.roulette_wheel[0] = 0
        i = 0
        for individual in self.population:
            s += individual.fitness
            if i < POP_SIZE - 1:
                self.roulette_wheel[i+1] = s
            i += 1
        # print(self.roulette_wheel, s)
        self.roulette_wheel = self.roulette_wheel / s

    def _select_parent(self):
        """roulette wheel selection"""
        prob = np.random.uniform()
        # print(max(np.searchsorted(self.roulette_wheel, prob, "right")-1, 0))
        p1 = self.population[max(np.searchsorted(self.roulette_wheel, prob, "right")-1, 0)]
        prob = np.random.uniform()
        p2 = self.population[max(np.searchsorted(self.roulette_wheel, prob, "right") - 1, 0)]
        while p2 == p1:
            prob = np.random.uniform()
            p2 = self.population[max(np.searchsorted(self.roulette_wheel, prob, "right") - 1, 0)]
        return p1, p2

    def _crossover(self, p1: Individual, p2: Individual):
        """PMX crossover"""
        first = np.random.randint(self.number_of_nodes-1)
        second = np.random.randint(first+1, self.number_of_nodes)
        gen1 = [0 for _ in range(self.number_of_nodes)]
        gen2 = [0 for _ in range(self.number_of_nodes)]
        gen1[first:second] = p1.gen[first:second]
        gen2[first:second] = p2.gen[first:second]
        check1 = defaultdict(bool)
        check2 = defaultdict(bool)
        for i in range(first, second):
            check1[p1.gen[i]] = True
            check2[p2.gen[i]] = True
        remain1 = [i for i in p2.gen if not check1[i]]
        remain2 = [i for i in p1.gen if not check2[i]]
        gen1[:first] = remain1[:first]
        gen1[second:] = remain1[first:]
        gen2[:first] = remain2[:first]
        gen2[second:] = remain2[first:]
        # print(p1.gen[first:second], p2.gen[first: second], remain1, remain2, gen1, gen2)

        return gen1, gen2

    def crossover_all(self):
        self._build_roulette_wheel()
        new_pop = []
        for _ in range(len(self.population)):
            if np.random.random() <= self.cx_prob:
                p1, p2 = self._select_parent()
                gen1, gen2 = self._crossover(p1, p2)
                new_pop.append(Individual(gen1))
                new_pop.append(Individual(gen2))
        self.set_pop_fitness(new_pop)
        new_pop.extend(self.population)
        self.population = sorted(new_pop, key=lambda x: x.fitness, reverse=True)[:POP_SIZE]
        return self.population[0]

    def _mutation(self, individual: Individual):
        """exchange 2 segments"""
        cut = np.random.randint(self.number_of_nodes)
        gen = copy.copy(individual.gen)
        individual.gen[:self.number_of_nodes - cut] = gen[cut:]
        individual.gen[self.number_of_nodes - cut:] = gen[:cut]
        individual.fitness = self._get_fitness(individual)
        return individual

    def mutation_all(self):
        for i in range(len(self.population)):
            if np.random.uniform() <= self.mutation_prob:
                self.population[i] = self._mutation(self.population[i])

    def loop(self):
        for _ in range(self.loop_count):
            self.mutation_all()
            individual = self.crossover_all()
            if individual.fitness > self.best_individual.fitness:
                self.best_individual = copy.copy(individual)
        return self.best_individual
