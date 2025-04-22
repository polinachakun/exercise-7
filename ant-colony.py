import numpy as np
import random
from environment import Environment
from ant import Ant

# Class representing the ant colony
"""
    ant_population: the number of ants in the ant colony
    iterations: the number of iterations 
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
    rho: pheromone evaporation rate
"""
class AntColony:
    def __init__(self, ant_population: int, iterations: int, alpha: float, beta: float, rho: float):
        self.ant_population = ant_population
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

        # Initialize the environment of the ant colony
        self.environment = Environment(self.rho, self.ant_population)

        # Initilize the list of ants of the ant colony
        self.ants = []

        # Initialize the ants of the ant colony
        for i in range(ant_population):
            # Initialize an ant on a random initial location from the possible locations
            initial_location = random.choice(self.environment.get_possible_locations())
            ant = Ant(self.alpha, self.beta, initial_location)

            # Position the ant in the environment of the ant colony so that it can move around
            ant.join(self.environment)

            # Add the ant to the ant colony
            self.ants.append(ant)

    # Solve the ant colony optimization problem
    def solve(self):
        """
        Run the Ant System algorithm to solve the TSP instance
        Returns:
            solution: list of cities in the best tour found
            shortest_distance: length of the best tour found
        """
        solution = []
        shortest_distance = float('inf')

        # Run for specified number of iterations
        for iteration in range(self.iterations):
            # For each iteration, have all ants construct a tour
            for ant in self.ants:
                # Randomly place ant on a city to start its tour
                ant.current_location = random.choice(self.environment.get_possible_locations())
                # Have the ant construct a complete tour
                ant.run()

                # Update best solution if this ant found a better tour
                if ant.traveled_distance < shortest_distance:
                    shortest_distance = ant.traveled_distance
                    solution = ant.visited.copy()

            self.environment.update_pheromone_map(self.ants)

            if (iteration + 1) % 10 == 0:
                print(f"Iteration {iteration + 1}/{self.iterations}, Best distance so far: {shortest_distance:.2f}")

        return solution, shortest_distance


def main():
    # Intialize the ant colony
    ant_colony = AntColony(
    ant_population=48,
    iterations=100,
    alpha=1.0,
    beta=5.0,
    rho=0.5
)

    # Solve the ant colony optimization problem
    solution, distance = ant_colony.solve()
    print("Solution: ", solution)
    print("Distance: ", distance)


if __name__ == '__main__':
    main()    