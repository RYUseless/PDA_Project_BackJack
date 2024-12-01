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

        agent = BlackjackAgent(
        self,
        learning_rate=0.01,
        min_learning_rate = 0.001,
        lr_decay = 0.95,
        initial_epsilon = 1.0,
        epsilon_decay = 0.95,
        final_epsilon = 0.1,    )
        # Data pro vizualizaci
        for episode in range(10):
            obs = env.reset()  # Reset prostředí, získání startovního stavu
            done = False
            player_cards = []
            dealer_cards = []
            moves = []
            reward = 0
            while not done:
                action = agent.get_action(self.env,obs)
                moves.append(action)
                obs, reward, done, _, _ = env.step(action)
                if len(player_cards) == 0:
                    player_cards.append(obs[0])
                if len(dealer_cards) == 0:
                    dealer_cards.append(obs[1])

            result = 0  # Initialize to 0 (draw)
            if reward > 0:
                result = 1  # Win
            elif reward < 0:
                result = -1  # Loss

            # Uložení výsledků
            self.results.append({
                "episode": episode + 1,
                "player_cards": player_cards,
                "dealer_cards": dealer_cards,
                "moves": result  # This line is changed
            })
    def graph(self, results):
        df = pd.DataFrame(results)

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

# Create an instance of the Visualize class
visualizer = Visualize(BlackjackAgent, gym.make('Blackjack-v1', render_mode="human"))


visualizer.games()
visualizer.graph(visualizer.results)