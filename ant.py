
# Class representing an artificial ant of the ant colony
"""
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
"""
class Ant():
    def __init__(self, alpha: float, beta: float, initial_location):
        self.alpha = alpha
        self.beta = beta
        self.current_location = initial_location
        self.traveled_distance = 0
        self.visited = []
        self.environment = None

    # The ant runs to visit all the possible locations of the environment
    def run(self):

            # Reset ant's memory for a new tour
            self.visited = [self.current_location]
            self.traveled_distance = 0

            # Visit all cities
            while len(self.visited) < len(self.environment.get_possible_locations()):
                next_city = self.select_path()
                self.traveled_distance += self.environment.get_distance(self.current_location, next_city)
                self.current_location = next_city
                self.visited.append(next_city)

            # Return to  starting city to complete  tour
            self.traveled_distance += self.environment.get_distance(self.current_location, self.visited[0])
            self.visited.append(self.visited[0])

    # Select the next path based on the random proportional rule of the ACO algorithm
    def select_path(self):

            # Get unvisited cities
            unvisited = list(set(self.environment.get_possible_locations()) - set(self.visited))

            # If no unvisited cities remain return to  start
            if not unvisited:
                return self.visited[0]

            # Calculate probabilities for each unvisited city
            probabilities = []
            for city in unvisited:
                pheromone = self.environment.get_pheromone(self.current_location, city)
                distance = self.environment.get_distance(self.current_location, city)

                # Avoid division by zero
                if distance == 0:
                    distance = 0.0001

                # Calculate probability based on pheromone and distance
                probability = (pheromone ** self.alpha) * ((1 / distance) ** self.beta)
                probabilities.append(probability)

            # Normalize probabilities
            total = sum(probabilities)
            if total == 0:
                return random.choice(unvisited)

            probabilities = [p / total for p in probabilities]

            # Select next city based on calculated probabilities
            next_city = random.choices(unvisited, weights=probabilities)[0]
            return next_city

    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment
    
    def get_distance(self, city1, city2):
             x1, y1 = self.environment.get_coordinates()[city1]
             x2, y2 = self.environment.get_coordinates()[city2]
             xd = x1 - x2
             yd = y1 - y2
             rij = math.sqrt((xd ** 2 + yd ** 2) / 10.0)
             return int(round(rij))
