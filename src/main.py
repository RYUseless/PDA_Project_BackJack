import src.utils.funny as InitialPrint
from src.utils.enviroment import Environment
import src.utils.helper as RyuHelp
from src.utils.visualization import Visualization


def main():
    funnyPrint_instance = InitialPrint.Greeter()
    funnyPrint_instance.run()

    print("\nBlackJack Model training: MPC-PDA-SEMESTRAL PROJECT")  # middle step between funny.py and environment.py :)
    help_inst = RyuHelp.MainHelper()
    user_input = help_inst.get_user_input()

    # if user input is Yes → pick 10 iteration
    # else if user input Nope → only one
    iterations = 1 if not user_input else 10

    env = None  # needed for env in else statement
    for counter in range(iterations):
        if user_input:  # if user input is True, aka 10loop testing
            print(f"\nRun numero: {counter}")
        env = Environment()
        env.train_agent()
        env.close_env()

        if user_input:  # if user input is True, aka 10loop testing
            val1, val2, val3 = env.get_results()
            help_inst.get_run_percentage(val1, val2, val3)

    if user_input:
        help_inst.get_avarage()
    else:
        Visualization.plot_training(env, env.agent)


if __name__ == "__main__":
    main()
