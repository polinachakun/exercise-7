import tsplib95
import numpy as np
import math

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
        self.problem = tsplib95.load('att48-specs/att48.tsp')
        self.num_nodes = len(self.problem.node_coords)

        # Create coordinates and distances maps
        self.coordinates = {}
        for node in self.problem.node_coords:
            # Node coordinates are 1-indexed in tsplib95
            self.coordinates[node-1] = self.problem.node_coords[node]

        # Calculate all distances using pseudo-euclidean metric
        self.distances = np.zeros((self.num_nodes, self.num_nodes))
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if i != j:
                    self.distances[i][j] = self.calculate_distance(i, j)

        # Initialize the pheromone map in the environment
        self.pheromone_map = None
        self.initialize_pheromone_map()

    def calculate_distance(self, i, j):

        # Get coordinates (converting from 0-based to 1-based indexing for tsplib95)
        x1, y1 = self.coordinates[i]
        x2, y2 = self.coordinates[j]

        # Pseudo-euclidean distance calculation
        xd = x1 - x2
        yd = y1 - y2
        rij = math.sqrt((xd * xd + yd * yd) / 10.0)
        tij = int(round(rij))
        return tij

    def initialize_pheromone_map(self):

        avg_distance = np.mean(self.distances[self.distances > 0])
        est_nn_tour_cost = avg_distance * self.num_nodes
        tau0 = self.ant_population / (self.num_nodes * est_nn_tour_cost)

        # Initialize all pheromone trails to tau0
        self.pheromone_map = np.full((self.num_nodes, self.num_nodes), tau0)

    def update_pheromone_map(self, ants):

        # Step 1: Pheromone evaporation on all edges
        self.pheromone_map *= (1 - self.rho)

        # Step 2: Pheromone deposit from all ants
        for ant in ants:
            # Skip if ant doesn't have a valid tour
            if not ant.visited or ant.traveled_distance <= 0:
                continue

            # Calculate pheromone deposit based on tour quality
            pheromone_deposit = 1 / ant.traveled_distance

            # Add pheromone to each edge in ant's tour
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
