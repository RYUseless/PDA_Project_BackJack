# agent.py
from collections import defaultdict
import numpy as np


class BlackjackAgent:
    def __init__(
            self,
            env,
            learning_rate: float,
            initial_epsilon: float,
            epsilon_decay: float,
            final_epsilon: float,
            discount_factor: float = 0.95,
    ):
        """Inicializuje agenta pro Q-learning s prázdnou Q-tabulkou a hyperparametry."""
        self.q_values = defaultdict(lambda: np.zeros(env.env.action_space.n))
        self.lr = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon
        self.training_error = []

    def get_action(self, env, obs: tuple[int, int, bool]) -> int:
        """Vrací akci s nejvyšší hodnotou nebo náhodnou akci pro zajištění průzkumu."""
        if np.random.random() < self.epsilon:
            return env.env.action_space.sample()
        else:
            return int(np.argmax(self.q_values[obs]))

    def update(self, obs, action, reward, terminated, next_obs):
        """Aktualizuje hodnotu Q-funkce pro zvolenou akci."""
        future_q_value = (not terminated) * np.max(self.q_values[next_obs])
        temporal_difference = reward + self.discount_factor * future_q_value - self.q_values[obs][action]
        self.q_values[obs][action] += self.lr * temporal_difference
        self.training_error.append(temporal_difference)

    def decay_epsilon(self):
        """Postupně snižuje epsilon pro zajištění většího využívání naučené politiky."""
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)
