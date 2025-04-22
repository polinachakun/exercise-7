import numpy as np

# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
    ant_population: number of ants in colony
"""
class Environment:
    def __init__(self, rho, ant_population):
        self.rho = rho
        self.ant_population = ant_population

        # Initialize the environment topology
        self.coordinates = self.load_coordinates("att48-specs/att48_coordinates.txt")
        self.distances = self.load_distances("att48-specs/att48_distance_matrix.txt")
        self.num_nodes = len(self.coordinates)

        # Initialize the pheromone map in the environment
        self.pheromone_map = None
        self.initialize_pheromone_map()

    def load_coordinates(self, filename):
        coords = []
        with open(filename, 'r') as f:
            for line in f:
                x, y = map(float, line.strip().split())
                coords.append((x, y))
        return coords

    def load_distances(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        matrix = [list(map(float, line.strip().split())) for line in lines]
        return np.array(matrix)

    def initialize_pheromone_map(self):
            """
            Initialize pheromone trails to a small positive value to ensure that the probability
            of choosing any edge in the initial stage is non-zero.

            The value is calculated as: tau0 = m / (n * C_nn)
            where:
                m = number of ants
                n = number of nodes
                C_nn = cost of nearest neighbor tour (estimated as average distance * num_nodes)
            """
            avg_distance = np.mean(self.distances[self.distances > 0])
            est_nn_tour_cost = avg_distance * self.num_nodes
            tau0 = self.ant_population / (self.num_nodes * est_nn_tour_cost)

            # Initialize all pheromone trails to tau0
            self.pheromone_map = np.full((self.num_nodes, self.num_nodes), tau0)

    def update_pheromone_map(self, ants):
            """
            Update pheromone trails based on the Ant System algorithm:
            1. Evaporate pheromone on all edges
            2. Deposit new pheromone based on the quality of solutions found by ants

            Args:
                ants: List of Ant objects that have completed their tours
            """
            # Step 1: Pheromone evaporation on all edges
            self.pheromone_map *= (1 - self.rho)

            # Step 2: Pheromone deposit from all ants
            for ant in ants:
                # Skip if ant doesn't have a valid tour
                if not ant.visited or ant.traveled_distance <= 0:
                    continue

                # Calculate pheromone deposit based on tour quality
                pheromone_deposit = 1 / ant.traveled_distance

                # Add pheromone to each edge in  ant's tour
                for i in range(len(ant.visited) - 1):
                    a, b = ant.visited[i], ant.visited[i+1]
                    self.pheromone_map[a][b] += pheromone_deposit
                    self.pheromone_map[b][a] += pheromone_deposit  # Symmetric TSP

    def get_pheromone(self, i, j):
        return self.pheromone_map[i][j]

    def get_distance(self, i, j):
        return self.distances[i][j]

    def get_possible_locations(self):
        return list(range(self.num_nodes))

    def get_coordinates(self):
        return self.coordinates
