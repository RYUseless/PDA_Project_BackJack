# environment.py

import gymnasium as gym
from collections import deque
# import numpy as np
from tqdm import tqdm
from src.utils.agent import BlackjackAgent
from src.utils.visualization import Visualization


class Environment:
    def __init__(self, n_episodes=100_000, learning_rate=0.01, start_epsilon=1.0, epsilon_decay=None,
                 final_epsilon=0.1):
        """Inicializuje prostředí Blackjack a agenta."""
        self.reward = 0
        self.env = gym.make("Blackjack-v1", sab=True)
        self.return_queue = deque(maxlen=n_episodes)
        self.length_queue = deque(maxlen=n_episodes)

        # Inicializace agenta
        self.agent = BlackjackAgent(
            env=self.env,
            learning_rate=learning_rate,
            initial_epsilon=start_epsilon,
            epsilon_decay=epsilon_decay if epsilon_decay else start_epsilon / (n_episodes / 2),
            final_epsilon=final_epsilon,
        )

        # Počítadla pro výhry
        self.player_wins = 0
        self.dealer_wins = 0
        self.draws = 0

    def update_results(self, result):
        """Aktualizace skóre po každé epizodě."""
        if result == 'player':
            self.player_wins += 1
        elif result == 'dealer':
            self.dealer_wins += 1
        elif result == 'draw':
            self.draws += 1

    def train_agent(self, n_episodes=100_000):
        """Trénuje agenta na definovaný počet epizod."""
        for episode in tqdm(range(n_episodes)):
            obs, info = self.env.reset()
            done = False
            episode_length = 0  # Počet kroků v aktuální epizodě
            result = None

            # Hrajeme jednu epizodu
            while not done:
                action = self.agent.get_action(self.env, obs)
                next_obs, self.reward, terminated, truncated, info = self.env.step(action)

                # Aktualizace agenta
                self.agent.update(obs, action, self.reward, terminated, next_obs)

                # Kontrola ukončení epizody
                done = terminated or truncated
                obs = next_obs
                episode_length += 1  # Počítání délky epizody

            # Určení výsledku epizody
            if int(self.reward) > 0:
                result = 'player'  # Hráč vyhrál
            elif int(self.reward) < 0.0:
                result = 'dealer'  # Dealer vyhrál
            else:
                result = 'draw'  # Remíza

            # Aktualizuj výsledky
            self.update_results(result)

            # Sledujeme odměny a délky epizod
            self.return_queue.append(self.reward)
            self.length_queue.append(episode_length)

            # Po každé epizodě nebudeme tisknout výsledek, souhrn se zobrazí na konci

            # Snižujeme epsilon
            self.agent.decay_epsilon()

        # Po dokončení všech epizod vypíšeme souhrn
        self.print_final_results()

        # Vizualizace tréninkového průběhu
        Visualization.plot_training(self, self.agent)  # Předáme jak self (enviroment), tak self.agent

    def print_final_results(self):
        """Vypíše konečné výsledky po trénování."""
        print("\nTrénování dokončeno! Výsledky:")
        print(f"\nKonečné skóre po {len(self.return_queue)} epizodách:")
        print(f"Hráč vyhrál {self.player_wins}x")
        print(f"Dealer vyhrál {self.dealer_wins}x")
        print(f"Remízy: {self.draws}x")


