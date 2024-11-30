import gymnasium as gym
import matplotlib.pyplot as plt
import pandas as pd

from src.utils.agent import BlackjackAgent


class Visualize:
    def __init__(self,agent,env):

        self.agent = agent
        self.env = env
        self.results = []

    def games(self):
        self.results = []
        # Inicializace prostředí Blackjack
        env = gym.make('Blackjack-v1', render_mode="human")
        agent = BlackjackAgent
        # Data pro vizualizaci
        for episode in range(10):
            obs = self.env.reset()[0]  # Reset prostředí, získání startovního stavu
            done = False
            player_cards = []
            dealer_cards = []
            moves = []
            while not done:
                action = agent.get_action(self.agent, env, obs)
                moves.append(action)
                obs, reward, done, _, _ = env.step(action)
                if len(player_cards) == 0:
                    player_cards.append(obs[0])
                if len(dealer_cards) == 0:
                    dealer_cards.append(obs[1])

            # Uložení výsledků
            self.results.append({
                "episode": episode + 1,
                "player_cards": player_cards,
                "dealer_cards": dealer_cards,
                "moves": moves
            })
    def graph(self, moves):
        # Převod dat do DataFrame
        df = pd.DataFrame(moves)

        # Vizualizace výsledků
        fig, ax = plt.subplots(figsize=(8, 5))

        # Graf: Výsledek každé hry
        df['result'] = df['moves'].map({1: 'Výhry', 0: 'Remízy', -1: 'Prohry'})
        result_colors = {'Výhry': 'green', 'Remízy': 'orange', 'Prohry': 'red'}
        df['result'].value_counts().reindex(result_colors.keys()).plot(
            kind='bar',
            ax=ax,
            color=[result_colors[r] for r in result_colors.keys()]
        )
        ax.set_title("Výsledky her")
        ax.set_ylabel("Počet her", labelpad=20)
        ax.set_xlabel("Výsledky", labelpad=20)

        plt.tight_layout()
        plt.show()
