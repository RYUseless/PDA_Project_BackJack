# outside imports:
import src.funny.funny as InitialPrint
from src.utils.enviroment import Environment
import os
from concurrent.futures import ProcessPoolExecutor
# local imports:
import src.utils.helper as RyuHelp
import src.utils.jsonActions as ryu_JS
from src.utils.visualization import Visualization


def train_single_run(iteration, user_input):
    """Funkce pro jeden běh trénování."""
    print(f"Training model {iteration + 1} is running...")
    env = Environment()
    env.train_agent()

    # Vrací výsledky z trénování
    results = env.get_results() if user_input else None
    env.close_env()
    return results


def main():
    """Main function"""
    R_JS = ryu_JS.Actions()
    funnyPrint_instance = InitialPrint.Greeter()
    funnyPrint_instance.run()

    print("\nBlackJack Model training: MPC-PDA-SEMESTRAL PROJECT")  # middle step between funny.py and environment.py :)
    help_inst = RyuHelp.MainHelper()
    user_input = help_inst.get_user_input()

    """Decide, how many runs there should be"""
    number_of_model_runs = R_JS.read_config("number_of_models_trained", "count")
    iterations = (
        1 if not user_input  # user picked "n" to prompt, aka single run only
        else number_of_model_runs if number_of_model_runs is not None  # user picker 10, check if config value is not none
        else 10  # If none, default to 10
    )

    cpu_count = os.cpu_count()  # get number of THREADS

    if iterations > 1:  # If user picked 10run training
        # run Paralel training
        with ProcessPoolExecutor() as executor:
            total_batches = (iterations + cpu_count - 1) // cpu_count
            for batch_idx in range(total_batches):
                # get single batch size (if needed, there should be more than one batches)
                start_idx = batch_idx * cpu_count
                end_idx = min(start_idx + cpu_count, iterations)
                batch_size = end_idx - start_idx

                print(f"\n\nBatch {batch_idx + 1}/{total_batches}: Training {batch_size} models simultaneously...")

                # spouštění paralelních výpočtů, aka využijeme všech xyz vláken
                futures = [
                    executor.submit(train_single_run, start_idx + j, user_input)
                    for j in range(batch_size)
                ]

                # return results of EACH run back to helper.py
                for future in futures:
                    result = future.result()
                    if result:  # valid results filter (no none and shit i hope)
                        help_inst.get_run_percentage(*result)  # *value gets each value from arr and fowards it as it is

        # count the michael average
        help_inst.get_avarage()
    else:
        # If user picked only single training run
        env = Environment()
        env.train_agent()
        env.print_final_results()
        Visualization.plot_training(env, env.agent)

        """ Uložení agenta do souboru """
        env.save_agent("trained_blackjack_agent.pkl")

        """ Načtení agenta ze souboru """
        # env.load_agent("trained_blackjack_agent.pkl")

        env.close_env()


if __name__ == "__main__":
    """wannabe main"""
    main()

