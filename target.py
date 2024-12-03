import random
import numpy as np

class Target:
    def __init__(self, x, y, z, target_type, a_star=None):
        self.x = x
        self.y = y
        self.z = z
        self.target_type = target_type
        self.a_star = a_star

    def random_move(self, max_x, max_y):
        self.x = random.randint(0, max_x - 1)
        self.y = random.randint(0, max_y - 1)
        self.z = 0  # Ground target, z is always 0

    def move(self, drones, ground_vehicles):
        if self.target_type == 'a_star' and self.a_star:
            # For simplicity, we use the first drone as the goal
            goal = (drones[0].x, drones[0].y)
            path = self.a_star.find_path((self.x, self.y), goal)
            if path:
                self.x, self.y = path[0]  # Move to the next step in the path
                self.z = 0  # Ground target, z is always 0

