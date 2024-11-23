# outside imports:
import src.utils.funny as InitialPrint
from src.utils.enviroment import Environment
import os
from concurrent.futures import ProcessPoolExecutor
# local imports:
import src.utils.helper as RyuHelp
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
    funnyPrint_instance = InitialPrint.Greeter()
    funnyPrint_instance.run()

    print("\nBlackJack Model training: MPC-PDA-SEMESTRAL PROJECT")  # middle step between funny.py and environment.py :)
    help_inst = RyuHelp.MainHelper()
    user_input = help_inst.get_user_input()

    iterations = 1 if not user_input else 10  # decide between 10 runs and 1 run (user input)
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

        # count the michael avarage
        help_inst.get_avarage()
    else:
        # If user picked only single training run
        env = Environment()
        env.train_agent()
        env.print_final_results()
        Visualization.plot_training(env, env.agent)

        user_input2 = help_inst.get_user_input2()
        if user_input2:
            # Uložení agenta do souboru
            env.save_agent("trained_blackjack_agent.pkl")
        else:
            pass

        # Načtení agenta ze souboru
        #env.load_agent("trained_blackjack_agent.pkl")

        env.close_env()


if __name__ == "__main__":
    """wannabe main"""
    main()
