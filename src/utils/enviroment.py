# eviroment
import gymnasium as gym
from collections import deque
from tqdm import tqdm
# local imports
from src.utils.agent import BlackjackAgent
import src.utils.jsonActions as ryu_JS


class Environment:
    def __init__(self):
        self.agent = None
        self.__reward = 0
        self.__env = gym.make("Blackjack-v1", natural=True)  # 'natural=True' if you want to deal with aces correctly

        # Placeholder values for JSON load from config file
        # These values are None, because I am reading them from config.json in load_model_values
        # and basically there is also check for the values if they are none, if not, no more loading → less runtime!
        self.n_episodes = None
        self.learning_rate = None
        self.min_learning_rate = None
        self.lr_decay = None
        self.start_epsilon = None
        self.epsilon_decay = None
        self.final_epsilon = None
        # lmao python ahh pointer thingy or smthn idk i am cybersec student, bye
        self.dummy_pointer_arr = [
            "n_episodes", "learning_rate", "min_learning_rate", "lr_decay",
            "start_epsilon", "epsilon_decay", "final_epsilon"
        ]
        # Function call for loading configuration values
        self.initialize_model_and_agent()  # ← MODEL VALUES SETTER BASICALLY

        # Sledování průběhu epizod
        self.return_queue = deque(maxlen=self.n_episodes)
        self.length_queue = deque(maxlen=self.n_episodes)
        # Value that holds results for all possible outcomes:
        self.player_wins = 0
        self.dealer_wins = 0
        self.draws = 0
        # percentage values:
        self.__percentage_draw = None
        self.__percentage_player = None
        self.__percentage_dealer = None

    def initialize_model_and_agent(self):
        """Načítání hodnot modelu z JSON souboru pomocí funkce read_config"""
        R_JS = ryu_JS.Actions()
        # this abomination basically does check for all the needed values,
        # and then it skips them or load values from json
        for param_name in self.dummy_pointer_arr:
            # Get the current value of the parameter using getattr
            current_value = getattr(self, param_name)

            if current_value is None:
                # If value is None, load it using the read_config method
                loaded_value = R_JS.read_config("model_config", param_name)
                setattr(self, param_name, loaded_value)

        # After loading values, perform checks
        if self.n_episodes is None or self.n_episodes <= 0:
            raise ValueError("n_episodes musí být kladné celé číslo.")
        if not (0 < self.learning_rate <= 1.0):
            raise ValueError("learning_rate musí být v intervalu (0, 1].")
        if not (0 < self.epsilon_decay <= 1.0):
            raise ValueError("epsilon_decay musí být v intervalu (0, 1].")
        if not (0 <= self.final_epsilon < self.start_epsilon):
            raise ValueError("final_epsilon musí být >= 0 a menší než start_epsilon.")

        """ AGENT VALUES INITIALIZATION"""
        self.agent = BlackjackAgent(
            env=gym.make("Blackjack-v1", natural=True),
            learning_rate=self.learning_rate,
            min_learning_rate=self.min_learning_rate,
            lr_decay=self.lr_decay,
            initial_epsilon=self.start_epsilon,
            epsilon_decay=self.epsilon_decay,
            final_epsilon=self.final_epsilon,
        )

    def update_results(self, result):
        """Update the score after each episode"""
        if result == 'player':
            self.player_wins += 1
        elif result == 'dealer':
            self.dealer_wins += 1
        elif result == 'draw':
            self.draws += 1

    def player_reward(self, player_sum, action, done, episode_count):
        """Calculate the reward for the player"""
        penalty_factor = min(episode_count / self.n_episodes, 1.0)

        """ Negative rewards"""
        if player_sum > 21:
            self.__reward -= 1.0  # Penalty for overshooting 21
        if action == 1 and 19 <= player_sum < 21:
            self.__reward -= 0.5 * penalty_factor  # Risky to hit when close to 21
        if action == 0 and player_sum < 15:
            self.__reward -= 0.3 * penalty_factor  # Too conservative standing too early
        if player_sum <= 10 and done:
            self.__reward -= 0.7 * penalty_factor  # Poor performance finishing with low sum
        if player_sum < 17 and not done:
            self.__reward -= 0.2  # Discourage waiting indefinitely in low-risk zones

        """Positive rewards"""
        if player_sum == 21:
            self.__reward += 1.0  # Perfect blackjack
        if 19 <= player_sum < 21:
            self.__reward += 0.5  # Not blackjack, but close enough
        if action == 0 and 17 <= player_sum < 21:
            self.__reward += 0.4  # Standing at a safe value
        if 15 <= player_sum < 17:
            self.__reward += 0.3  # Gradual improvement
        if action == 1 and player_sum < 12:
            self.__reward += 0.2  # Encouragement to hit with low sum
        if action == 0 and 18 <= player_sum < 20:
            self.__reward += 0.4  # Reward standing between 18-19
        if action == 0 and player_sum == 20:
            self.__reward += 0.25  # Reward for standing exactly at 20

        """ Additional context-based adjustments"""
        if action == 1 and 13 <= player_sum <= 16:
            self.__reward += 0.1  # Slight aggression (hitting) when safe
        if action == 1 and player_sum <= 8:
            self.__reward -= 0.2  # Light penalty for overconfidence with low sum
        if not done and 12 <= player_sum <= 14:
            self.__reward += 0.05  # Neutralize small penalties if the player is still trying

    def train_agent(self):
        """Train the agent for a specified number of episodes"""
        for one_round in tqdm(range(self.n_episodes)):
            obs, info = self.__env.reset()
            done = False
            episode_length = 0

            while not done:
                action = self.agent.get_action(self.__env, obs)
                next_obs, self.__reward, terminated, truncated, info = self.__env.step(action)

                # Reward calculation
                player_sum = obs[0]
                self.player_reward(player_sum, action, done, one_round)

                # Update agent
                self.agent.update(obs, action, self.__reward, terminated, next_obs)

                # Check if the episode is done
                done = terminated or truncated
                obs = next_obs
                episode_length += 1

            # Determine result and update scores
            if float(self.__reward) > 0.0:
                result = 'player'
            elif float(self.__reward) < 0.0:
                result = 'dealer'
            else:
                result = 'draw'

            self.update_results(result)

            # Track rewards and episode lengths
            self.return_queue.append(self.__reward)
            self.length_queue.append(episode_length)

            # Decay epsilon
            self.agent.decay_epsilon()

        # After all episodes, calculate percentages
        self.__percentage_player = round((self.player_wins / len(self.return_queue)) * 100, 1)
        self.__percentage_dealer = round((self.dealer_wins / len(self.return_queue)) * 100, 1)
        self.__percentage_draw = round((self.draws / len(self.return_queue)) * 100, 1)

    def print_final_results(self):
        print("\nVýsledek natrénovaného modelu po %s epizodách:" % len(self.return_queue))
        print(f"Výhry hráče: {self.player_wins}x, což odpovídá: {self.__percentage_player}% úspěšnosti.")
        print(f"Výhry dealera {self.dealer_wins}x, což odpovídá: {self.__percentage_dealer}% úspěšnosti.")
        print(f"Remízy, aka nevyhrál nikdo: {self.draws}x, což je {self.__percentage_draw}%.")

    def get_results(self):
        return self.__percentage_player, self.__percentage_dealer, self.__percentage_draw

    def close_env(self):
        self.__env.close()

    # Methods for saving and loading agent
    def save_agent(self, file_path):
        self.agent.save_policy(file_path)

    def load_agent(self, file_path):
        self.agent.load_policy(file_path)


