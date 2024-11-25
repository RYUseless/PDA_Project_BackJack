import gymnasium as gym
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

# Inicializace prostředí Blackjack
env = gym.make('Blackjack-v1', render_mode="human")

# Data pro vizualizaci
results = []

# Odehrání 10 her
for episode in range(10):
    obs = env.reset()[0]  # Reset prostředí, získání startovního stavu
    done = False
    player_cards = []
    dealer_cards = []
    while not done:
        action = 1 if obs[0] < 17 else 0  # Jednoduchá strategie
        obs, reward, done, _, _ = env.step(action)
        if len(player_cards) == 0:
            player_cards.append(obs[0])
        if len(dealer_cards) == 0:
            dealer_cards.append(obs[1])

    # Uložení výsledků
    results.append({
        "episode": episode + 1,
        "player_cards": player_cards,
        "dealer_cards": dealer_cards,
        "reward": reward
    })

# Převod dat do DataFrame
df = pd.DataFrame(results)

# Výpočet četnosti karet
player_card_counts = Counter(card for row in df['player_cards'] for card in row)
dealer_card_counts = Counter(card for row in df['dealer_cards'] for card in row)

# Vizualizace výsledků
fig, ax = plt.subplots(figsize=(8, 5))

# Graf: Výsledek každé hry
df['result'] = df['reward'].map({1: 'Výhry', 0: 'Remízy', -1: 'Prohry'})
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

# Výpis četností karet
print("Hodnoty dosažené hráčem:")
for card, count in sorted(player_card_counts.items()):
    print(f"Celková hodnota karet {card}: {count}x")

print("\nHodnoty dosažené krupiérem:")
for card, count in sorted(dealer_card_counts.items()):
    print(f"Hodnota viditelné karty {card}: {count}x")