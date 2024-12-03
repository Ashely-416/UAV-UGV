import numpy as np
from env import Environment, generate_obstacle_map_from_csv
from target import Target
from A3CAgent import A3CAgent

# Example target definitions
targets = [
    Target(x=10, y=10, z=0, target_type='static'),
    Target(x=20, y=20, z=0, target_type='random'),
    Target(x=30, y=30, z=0, target_type='a_star')
]

# Example wind field
wind_field = np.zeros((50, 50, 50))
wind_threshold = 5

# Generate obstacle map from CSV file
csv_file = 'real_city_grid_map.csv'
num_grids = 50
max_height = 50
obstacle_map = generate_obstacle_map_from_csv(csv_file, num_grids, max_height)

# Create environment instance
env = Environment(obstacle_map, targets, wind_field, wind_threshold, num_drones=4, num_ground_vehicles=1)
env.reset()

# Initialize A3C agent for drones
drone_agent = A3CAgent(input_dim=6, action_space=8)

# Example run loop
num_steps = 100
num_episodes = 10
total_rewards = []
coverage_rates = []

for episode in range(num_episodes):
    env.reset()
    total_reward = 0
    searched_area = set()
    coverage_rate = 0  # Initialize coverage rate
    for step in range(num_steps):
        drone_states = [np.array([d.x, d.y, d.z, d.speed, d.observation_range, 0]) for d in env.drones]
        drone_actions = []
        drone_log_probs = []
        drone_values = []
        for state in drone_states:
            action, log_prob, value = drone_agent.select_action(state)
            drone_actions.append(action)
            drone_log_probs.append(log_prob)
            drone_values.append(value)

        env.step(drone_actions)

        for drone in env.drones:
            observed_pos = drone.observe(env.targets)
            if observed_pos:
                true_pos = (observed_pos[0], observed_pos[1], observed_pos[2])
                searched_area.update((drone.x, drone.y) for drone in env.drones)
                coverage_rate = len(searched_area) / (env.len * env.width)
                reward = drone_agent.compute_reward(observed_pos, true_pos, coverage_rate)
                total_reward += reward
                print(f"Step {step}, Reward: {reward}, Drone Position: ({drone.x}, {drone.y}, {drone.z}), "
                      f"Observed Position: {observed_pos}, True Position: {true_pos}, Coverage Rate: {coverage_rate}")
                break

        # Collect rewards for training
        rewards = [drone_agent.compute_reward(observed_pos, true_pos, coverage_rate) if observed_pos else 0 for _ in env.drones]

        # Store trajectory
        trajectory = zip(drone_states, drone_actions, rewards, drone_log_probs, drone_values)
        drone_agent.update(trajectory, targets, env)

    total_rewards.append(total_reward)
    coverage_rates.append(coverage_rate)
    print(f"Episode {episode}, Total Reward: {total_reward}, Coverage Rate: {coverage_rate}")

print("Training complete.")





