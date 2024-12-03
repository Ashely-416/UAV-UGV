import numpy as np
from env import Environment, generate_obstacle_map_from_csv
from A3CAgent import A3CAgent
from DDPGAgent import DDPGAgent
from config import config

def main():
    obstacle_map = generate_obstacle_map_from_csv('real_city_grid_map.csv', 50, 50)
    wind_field = np.zeros((50, 50, 50))  # Example wind field
    wind_threshold = 5  # Example threshold

    env = Environment(obstacle_map, config['targets'], wind_field, wind_threshold, num_drones=5, num_ground_vehicles=5)
    env.reset()

    if config['algorithm'] == 'A3C':
        agent = A3CAgent(input_dim=6, action_space=8)
    elif config['algorithm'] == 'DDPG':
        agent = DDPGAgent(input_dim=6, action_space=2)  # Example dimensions for DDPG

    num_steps = config['num_steps']
    num_episodes = config['num_episodes']
    total_rewards = []
    coverage_rates = []

    for episode in range(num_episodes):
        env.reset()
        total_reward = 0
        searched_area = set()
        for step in range(num_steps):
            drone_states = [np.array([d.x, d.y, d.z, d.speed, d.observation_range, 0]) for d in env.drones]
            drone_actions = []
            drone_log_probs = []
            drone_values = []

            for state in drone_states:
                action, log_prob, value = agent.select_action(state)
                drone_actions.append(action)
                drone_log_probs.append(log_prob)
                drone_values.append(value)

            env.step(drone_actions)

            for drone in env.drones:
                observed_pos = drone.observe(env.targets[0]['instance'])
                if observed_pos:
                    true_pos = (env.targets[0]['instance'].x, env.targets[0]['instance'].y)
                    searched_area.update((drone.x, drone.y) for drone in env.drones)
                    coverage_rate = len(searched_area) / (env.len * env.width)
                    reward = agent.compute_reward(observed_pos, true_pos, coverage_rate, drone.observation_range)
                    total_reward += reward
                    break

            rewards = [agent.compute_reward(observed_pos, true_pos, coverage_rate, drone.observation_range) if observed_pos else 0 for _ in env.drones]

            trajectory = zip(drone_states, drone_actions, rewards, drone_log_probs, drone_values)
            agent.update(trajectory)

        total_rewards.append(total_reward)
        coverage_rates.append(coverage_rate)
        print(f"Episode {episode}, Total Reward: {total_reward}, Coverage Rate: {coverage_rate}")

    print("Training complete.")

if __name__ == "__main__":
    main()
