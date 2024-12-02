# Výchozí balíček je definován v globálu/ jeho modifikaci pro speciální pravidla/testování?
# Fitness funkce/genetické programování nesmí vidět hodnoty karet, eliminovalo by to aspekt náhody
# Omezení dealera ( stát na 17, nebrat dál po převýšení hráčovy sumy?)
# Řešení probíhá pouze pro dvě karty, prokonzultovat se zbytkem jak to napojit na funkci která umožní další tah

import random


class Generation:
    def __init__(self):
        print("\n\033[1m\u2022 Card Generation:\033[0m")
        self.__deck = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8,
                       9, 9, 9, 9, 10,
                       10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

    def _setup(self):
        shuffle = random.randint(1, 9)
        while shuffle > 0:
            random.shuffle(self.__deck)
            shuffle -= 1
        self._play()

    def _play(self):
        player_hand = []
        dealer_hand = []

        # Deal initial two cards
        for _ in range(2):
            player_hand.append(self.__deck.pop(0))
            dealer_hand.append(self.__deck.pop(0))

        player_sum = self._calculate_hand(player_hand)
        dealer_sum = self._calculate_hand(dealer_hand)

        print("\tHodnota hráčovy ruky je :", player_sum)
        # print("\tHodnota krupiérovy ruky je:", dealer_sum)

        # Check for initial blackjack
        if player_sum == 21 and dealer_sum < 21:
            print("\tHráč má blackjack, vítězí hráč")
            return
        elif dealer_sum == 21 and player_sum < 21:
            print("\tKrupiér má blackjack, vítězí krupiér")
            return

        # Player turn
        while player_sum < 21:
            action = input("\tChcete další kartu? (ano/ne): ").strip().lower()
            if action == 'ano':
                player_hand.append(self.__deck.pop(0))
                player_sum = self._calculate_hand(player_hand)
                print("\tHodnota hráčovy ruky je :", player_sum)
            else:
                break

        # Dealer turn
        while dealer_sum < 17:
            dealer_hand.append(self.__deck.pop(0))
            dealer_sum = self._calculate_hand(dealer_hand)
            print("\tHodnota krupiérovy ruky je:", dealer_sum)

        # Determine winner
        if player_sum > 21:
            print("\tHráč přetáhl, vítězí krupiér")
        elif dealer_sum > 21:
            print("\tKrupiér přetáhl, vítězí hráč")
        elif player_sum > dealer_sum:
            print("\tHráč vítězí")
        elif dealer_sum > player_sum:
            print("\tKrupiér vítězí")
        else:
            print("\tRemíza")

    @staticmethod
    def _calculate_hand(hand):
        total = 0
        ace_count = 0
        for card in hand:
            if card == 1:
                ace_count += 1
                total += 11
            else:
                total += card

        # Adjust for aces
        while total > 21 and ace_count > 0:
            total -= 10
            ace_count -= 1

        return total

    def run(self):
        self._setup()


