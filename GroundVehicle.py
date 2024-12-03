import random

class GroundVehicle:
    def __init__(self, x, y, environment, speed):
        self.x = x
        self.y = y
        self.environment = environment
        self.speed = speed
        # self.ground_observation_range = ground_observation_range
        self.step_size = 70  # Maximum step size for ground vehicles

    def move(self):
        # Random movement in 8 possible directions (N, NE, E, SE, S, SW, W, NW)
        movements = [
            (0, 1), (1, 1), (1, 0), (1, -1),
            (0, -1), (-1, -1), (-1, 0), (-1, 1)
        ]
        dx, dy = random.choice(movements)
        new_x = self.x + dx * self.step_size
        new_y = self.y + dy * self.step_size

        if 0 <= new_x < self.environment.len and 0 <= new_y < self.environment.width:
            if self.environment.obstacle_map[new_x, new_y, 0] == 0:
                self.x, self.y = new_x, new_y

