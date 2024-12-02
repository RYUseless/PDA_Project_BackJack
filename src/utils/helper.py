import gymnasium as gym


from src.utils.agent import BlackjackAgent
import src.utils.jsonActions as Ryu_JS
from src.utils.jsonActions import Actions


class MainHelper:
    def __init__(self):
        self.__player_percentage = []
        self.__dealer_percentage = []
        self.__draw_percentage = []
        R_JS = Ryu_JS.Actions()
        self.num_of_runs = R_JS.read_config("number_of_models_trained", "count")

    def get_user_input(self):
        attempts = 0  # Počet pokusů o správný vstup
        while attempts < 3:
            user_input = input("Zapnout trénování %s modelů zároveň? [y/n]" % self.num_of_runs).strip().lower()

            if user_input == 'y':
                return True  # Vstup je 'Y' nebo 'y', vrátí True
            elif user_input == 'n':
                return False  # Vstup je 'N' nebo 'n', vrátí False
            else:
                attempts += 1  # Zvýšíme počet pokusů
                print(f"Neplatný vstup. Pokus {attempts} z 3.")  # Oznámení o neplatném vstupu

        print("Příliš mnoho neplatných pokusů, vizualizace bude vypnuta.")
        return False  # Po třech neplatných pokusech, vrátí False

    def get_run_percentage(self, player_percentage, delaer_percentage, draw_percentage):
        self.__player_percentage.append(player_percentage)
        self.__dealer_percentage.append(delaer_percentage)
        self.__draw_percentage.append(draw_percentage)

    def get_avarage(self):
        print("\n\nVýsledky po %s runech:" % self.num_of_runs)
        # for some random reason my round did not work so i added 2f funny thing, but still kept round for round thingys
        print(
            f"Průměrná procentuální výhra hráče je: {round(sum(self.__player_percentage) / len(self.__player_percentage), 2):.2f}%")

        print(
            f"Průměrná procentuální výhra dealera je: {round(sum(self.__dealer_percentage) / len(self.__dealer_percentage), 2):.2f}%")

        print(
            f"Průměrná procentuální remíza je: {round(sum(self.__draw_percentage) / len(self.__draw_percentage), 2):.2f}%")


class Visualize:
    def __init__(self, env):

        self.config = Actions()
        self.env = env
        self.results = []

    def games(self):
        self.results = []
        # Inicializace prostředí Blackjack
        env = gym.make('Blackjack-v1', render_mode="human")

        agent = BlackjackAgent(
            self,
            learning_rate=self.config.read_config("model_config", "learning_rate"),
            min_learning_rate=self.config.read_config("model_config", "min_learning_rate"),
            lr_decay=self.config.read_config("model_config", "lr_decay"),
            initial_epsilon=self.config.read_config("model_config", "start_epsilon"),
            epsilon_decay=self.config.read_config("model_config", "epsilon_decay"),
            final_epsilon=self.config.read_config("model_config", "final_epsilon")
        )

        while True:
            try:
                start_episode = int(input("Enter the start episode for visualization: "))
                num_games = int(input("Enter the number of games to visualize: "))
                break
            except ValueError:
                print("Invalid input. Please enter number")

        # Data pro vizualizaci
        for episode in range(start_episode, start_episode + num_games):
            obs = env.reset()  # Reset prostředí, získání startovního stavu
            done = False
            player_cards = []
            dealer_cards = []
            moves = []
            reward = 0
            while not done:
                action = agent.get_action(env,obs)
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


