import gym
import numpy as np


def play_blackjack():
    env = gym.make('Blackjack-v1', natural=True, sab=True)
    observation = env.reset()
    print(f"První ruka: {observation}")

    done = False
    while not done:
        action = input("Chcete další kartu? ('h' pro hit, 's' pro stand): ").strip().lower()

        if action == 'h':
            action = 1  # Akce hit
        elif action == 's':
            action = 0  # Akce stand
        else:
            print("Neplatná akce. Použijte 'h' pro hit nebo 's' pro stand.")
            continue

        observation, reward, done, info = env.step(action)
        print(f"Obdrželi jste kartu: {observation}")

    if reward > 0:
        print("Vyhráli jste!")
    elif reward == 0:
        print("Remíza!")
    else:
        print("Prohráli jste!")


if __name__ == "__main__":
    play_blackjack()
