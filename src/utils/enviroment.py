# environment.py
import gymnasium as gym
from collections import deque
# import numpy as np
from tqdm import tqdm
from src.utils.agent import BlackjackAgent


class Environment:
    def __init__(self,
                 n_episodes=100_000,
                 learning_rate=0.01,
                 min_learning_rate=0.001,
                 lr_decay=0.9999,
                 start_epsilon=1.0,
                 epsilon_decay=0.95,
                 final_epsilon=0.1,
                 ):
        """
        Inicializuje prostředí Blackjack a agenta.

        Args:
            n_episodes (int): Počet epizod pro trénink agenta.
            learning_rate (float): Rychlost učení agenta.
            start_epsilon (float): Počáteční hodnota epsilonu pro epsilon-greedy strategii.
            epsilon_decay (float): Faktor, kterým se epsilon násobí po každé epizodě.
            final_epsilon (float): Minimální hodnota epsilonu.
        """
        # reality check for correct values in innit mate:
        if n_episodes <= 0:
            raise ValueError("n_episodes musí být kladné celé číslo.")
        if not (0 < learning_rate <= 1.0):
            raise ValueError("learning_rate musí být v intervalu (0, 1].")
        if not (0 < epsilon_decay <= 1.0):
            raise ValueError("epsilon_decay musí být v intervalu (0, 1].")
        if not (0 <= final_epsilon < start_epsilon):
            raise ValueError("final_epsilon musí být >= 0 a menší než start_epsilon.")

        self.__reward = 0
        self.__env = gym.make("Blackjack-v1", natural=True)  # sab → simple, natural → check for eso and shit
        self.__n_episodes = n_episodes

        # Sledování průběhu epizod
        self.return_queue = deque(maxlen=n_episodes)
        self.length_queue = deque(maxlen=n_episodes)

        # Inicializace agenta
        self.agent = BlackjackAgent(
            env=self.__env,
            learning_rate=learning_rate,
            min_learning_rate=min_learning_rate,
            lr_decay=lr_decay,
            initial_epsilon=start_epsilon,
            epsilon_decay=epsilon_decay,
            final_epsilon=final_epsilon,
        )

        # Statistiky pro výsledky
        self.player_wins = 0
        self.dealer_wins = 0
        self.draws = 0

        # other vals:
        self.__percentage_draw = None
        self.__percentage_player = None
        self.__percentage_dealer = None

    def update_results(self, result):
        """Aktualizace skóre po každé epizodě."""
        if result == 'player':
            self.player_wins += 1
        elif result == 'dealer':
            self.dealer_wins += 1
        elif result == 'draw':
            self.draws += 1

    def train_agent(self):
        """Trénuje agenta na definovaný počet epizod."""
        for _ in tqdm(range(self.__n_episodes)):
            obs, info = self.__env.reset()
            done = False
            episode_length = 0  # Počet kroků v aktuální epizodě

            # Hrajeme jednu epizodu
            while not done:
                action = self.agent.get_action(self.__env, obs)
                next_obs, self.__reward, terminated, truncated, info = self.__env.step(action)

                # Aktualizace agenta
                self.agent.update(obs, action, self.__reward, terminated, next_obs)

                # Kontrola ukončení epizody
                done = terminated or truncated
                obs = next_obs
                episode_length += 1  # Počítání délky epizody

            """
            záporný reward → dealer win
            kladný reward → player win
            reward == 0.0000 → remíza
            """
            if float(self.__reward) > 0.0:
                result = 'player'
            elif float(self.__reward) < 0.0:
                result = 'dealer'
            else:
                result = 'draw'

            # Aktualizuj výsledky
            self.update_results(result)

            # Sledujeme odměny a délky epizod
            self.return_queue.append(self.__reward)
            self.length_queue.append(episode_length)

            # Po každé epizodě nebudeme tisknout výsledek, souhrn se zobrazí na konci

            # Snižujeme epsilon
            self.agent.decay_epsilon()

        # Po dokončení všech epizod vypíšeme souhrn
        self.print_final_results()

    def print_final_results(self):
        self.__percentage_player = round((self.player_wins / len(self.return_queue)) * 100, 1)
        self.__percentage_dealer = round((self.dealer_wins / len(self.return_queue)) * 100, 1)
        self.__percentage_draw = round((self.draws / len(self.return_queue)) * 100, 1)

        print("\nTrénování dokončeno! Výsledky:")
        print(f"\nKonečné skóre po {len(self.return_queue)} epizodách:")
        print(f"Hráč vyhrál {self.player_wins}x, což odpovídá {self.__percentage_player}% úspěšnosti.")
        print(f"Dealer vyhrál {self.dealer_wins}x, což odpovídá {self.__percentage_dealer}% úspěšnosti.")
        print(f"Remízy: {self.draws}x, což odpovídá {self.__percentage_draw}% úspěšnosti.")

    def get_results(self):
        return self.__percentage_player, self.__percentage_dealer, self.__percentage_draw

    def close_env(self):
        self.__env.close()
