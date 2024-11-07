# main.py
import src.utils.funny as InitialPrint
from src.utils.enviroment import Environment
from src.utils.visualization import Visualization

if __name__ == "__main__":
    funnyPrint_instance = InitialPrint.Greeter()
    funnyPrint_instance.run()

    env = Environment()
    env.train_agent()
    Visualization.plot_training(env, env.agent)

