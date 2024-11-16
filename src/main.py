import src.utils.funny as InitialPrint
from src.utils.enviroment import Environment
from src.utils.visualization import Visualization


def main():
    funnyPrint_instance = InitialPrint.Greeter()
    funnyPrint_instance.run()

    print("\nBlackJack Model training: MPC-PDA-SEMESTRAL PROJECT")  # middle step between funny.py and environment.py :)

    env = Environment()
    env.train_agent()
    Visualization.plot_training(env, env.agent)


if __name__ == "__main__":
    main()
