import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Patch


class Visualization:
    @staticmethod
    def plot_training(env, agent, rolling_length=100):
        """Vizualizuje trénink pomocí grafu odměn, chybovosti a délky epizody."""

        # Reward Plot
        reward_moving_average = np.convolve(np.array(env.return_queue).flatten(), np.ones(rolling_length),
                                            mode='valid') / rolling_length
        plt.figure(figsize=(14, 10))

        # Plot odměn
        plt.subplot(2, 2, 1)
        plt.plot(reward_moving_average, label="Moving Average Reward", color='blue')
        plt.xlabel("Episode")
        plt.ylabel("Reward")
        plt.title("Reward per Episode (Moving Average)")
        plt.legend()

        # Error Plot (training error)
        plt.subplot(2, 2, 2)
        plt.plot(agent.training_error, label="Training Error", color='red')
        plt.xlabel("Episode")
        plt.ylabel("Error")
        plt.title("Agent's Training Error")
        plt.legend()

        # Výhry hráče vs dealera
        plt.subplot(2, 2, 3)
        plt.bar(['Player Wins', 'Dealer Wins', 'Draws'],
                [env.player_wins, env.dealer_wins, env.draws], color=['green', 'red', 'gray'])
        plt.ylabel("Count")
        plt.title("Player vs Dealer Wins")

        # Délka epizod (rolling length)
        length_moving_average = np.convolve(np.array(env.length_queue).flatten(), np.ones(rolling_length),
                                            mode='valid') / rolling_length
        plt.subplot(2, 2, 4)
        plt.plot(length_moving_average, label="Moving Average Episode Length", color='orange')
        plt.xlabel("Episode")
        plt.ylabel("Length")
        plt.title("Episode Length (Moving Average)")
        plt.legend()

        plt.tight_layout()
        plt.show(block=True)  # Blokuje program, dokud uživatel nezavře okno

        # Zavře grafické okno
        plt.close()

        # Ukončí program po zavření okna
        print("Graf zavřen. Program se ukončuje.")
        exit()

