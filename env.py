import csv
import numpy as np
from UAV import UAV
from GroundVehicle import GroundVehicle
from target import Target
from a_star import AStar

class Environment:
    def __init__(self, obstacle_map, targets, wind_field, wind_threshold, num_drones, num_ground_vehicles):
        self.obstacle_map = obstacle_map
        self.targets = targets
        self.wind_field = wind_field
        self.wind_threshold = wind_threshold
        self.num_drones = num_drones
        self.num_ground_vehicles = num_ground_vehicles
        self.len = obstacle_map.shape[0]
        self.width = obstacle_map.shape[1]
        self.height = obstacle_map.shape[2]
        self.drones = []
        self.ground_vehicles = []

    def reset(self):
        self.drones = []
        self.ground_vehicles = []
        for _ in range(self.num_drones):
            x, y, z = self.get_random_position()
            speed = 2  # Fixed speed
            observation_range = np.random.uniform(5, 15)  # Example observation range
            self.drones.append(UAV(x, y, z, speed, observation_range))

        for _ in range(self.num_ground_vehicles):
            x, y = self.get_random_position()[:2]
            speed = np.random.uniform(5, 10)  # Example speed range
            self.ground_vehicles.append(GroundVehicle(x, y, speed))

        for target in self.targets:
            if target['type'] == 'static':
                target['instance'] = Target(target['x'], target['y'], 0, target['type'])
            elif target['type'] == 'random':
                target['instance'] = Target(target['x'], target['y'], 0, target['type'])
            elif target['type'] == 'a_star':
                target['instance'] = Target(target['x'], target['y'], 0, target['type'], a_star=AStar(self.obstacle_map))

    def get_random_position(self):
        x, y, z = np.random.randint(self.len), np.random.randint(self.width), np.random.randint(self.height)
        while self.obstacle_map[x, y, z] == 1:
            x, y, z = np.random.randint(self.len), np.random.randint(self.width), np.random.randint(self.height)
        return x, y, z

    def step(self, drone_actions):
        drone_positions = [(drone.x, drone.y, drone.z) for drone in self.drones]
        for i, drone in enumerate(self.drones):
            drone.move(drone_actions[i], drone_positions)

        for vehicle in self.ground_vehicles:
            vehicle.move()

        for target in self.targets:
            if target['type'] == 'random':
                target['instance'].random_move(self.len, self.width)
            elif target['type'] == 'a_star':
                target['instance'].move(self.drones, self.ground_vehicles)

    def visualize_environment(self):
        pass  # Visualization code (if needed)

def generate_obstacle_map_from_csv(csv_file, num_grids, max_height):
    obstacle_map = np.zeros((num_grids, num_grids, max_height))
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            x, y, height = int(row['x']), int(row['y']), int(row['height'])
            obstacle_map[x, y, :height] = 1
    return obstacle_map

