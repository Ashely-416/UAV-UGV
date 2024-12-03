import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from UAV import UAV

class A3CNetwork(nn.Module):
    def __init__(self, input_dim, action_space):
        super(A3CNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.policy_head = nn.Linear(128, action_space)
        self.value_head = nn.Linear(128, 1)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, state):
        x = self.relu(self.fc1(state))
        x = self.relu(self.fc2(x))
        policy = self.softmax(self.policy_head(x))
        value = self.value_head(x)
        return policy, value

class A3CAgent:
    def __init__(self, input_dim, action_space):
        self.input_dim = input_dim
        self.action_space = action_space
        self.network = A3CNetwork(input_dim, action_space)
        self.optimizer = optim.Adam(self.network.parameters(), lr=1e-4)
        self.gamma = 0.99

    def select_action(self, state):
        state = torch.FloatTensor(state).unsqueeze(0)
        policy, value = self.network(state)
        action = np.random.choice(self.action_space, p=policy.detach().numpy()[0])
        log_prob = torch.log(policy.squeeze(0)[action])
        return action, log_prob, value

    def update(self, trajectory):
        states, actions, rewards, log_probs, values = zip(*trajectory)
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        log_probs = torch.stack(log_probs)
        values = torch.stack(values)

        returns = []
        R = 0
        for r in rewards[::-1]:
            R = r + self.gamma * R
            returns.insert(0, R)
        returns = torch.FloatTensor(returns)

        advantage = returns - values.squeeze(1)
        actor_loss = -(log_probs * advantage.detach()).mean()
        critic_loss = advantage.pow(2).mean()
        loss = actor_loss + critic_loss

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def compute_accuracy_reward(self, observed_pos,true_pos):
        distance = np.linalg.norm(np.array(observed_pos) - np.array(true_pos))
        if observed_pos == true_pos:
            return 100  # Example reward calculation
        elif distance <= UAV. self.observation_range:
            accuracy_reward = 40  # Within observation range
        else:
            accuracy_reward = -50  # Outside observation range
        return accuracy_reward

    def compute_reward(self, observed_pos, true_pos, coverage_rate):
        reward = self.compute_accuracy_reward(observed_pos,true_pos) + coverage_rate*50
        return reward

