# Výchozí balíček je definován v globálu/ jeho modifikaci pro speciální pravidla/testování?
# Fitness funkce/genetické programování nesmí vidět hodnoty karet, eliminovalo by to aspekt náhody
# Omezení dealera ( stát na 17, nebrat dál po převýšení hráčovy sumy?)
# Řešení probíhá pouze pro dvě karty, prokonzultovat se zbytkem jak to napojit na funkci která umožní další tah

import random


# from random import randint

class Generation:
    def __init__(self):
        print("\n\033[1m\u2022 Card Generation:\033[0m")
        self.__deck = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8,
                       9, 9, 9, 9, 10,
                       10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

    def setup(self):
        shuffle = random.randint(1, 9)
        while shuffle > 0:
            random.shuffle(self.__deck)
            shuffle -= 1
        self.asses()

    def asses(self):
        player = 0
        dealer = 0
        acep = 0
        aced = 0
        print("\tKontrola balíčku", self.__deck)
        for i in range(0, 2):
            player += self.__deck[0]
            if self.__deck[0] == 1:
                print("\tHráč vytáhl eso")
                if player < 11:
                    player += 10
                    acep += 1
            if (player > 21) and (acep == 1):
                player -= 10
            del self.__deck[0]
            dealer += self.__deck[0]
            if self.__deck[0] == 1:
                print("\tKrupiér vytáhl eso")
                if dealer < 11:
                    dealer += 10
                    aced += 1
            if (dealer > 21) and (aced == 1):
                dealer -= 10
            del self.__deck[0]
        print("\tHodnota hráčovy ruky je :", player)
        if player == 21:
            print("\tHráč má blackjack, vítězí hráč")
        print("\tHodnota krupiérovy ruky je:", dealer)
        if dealer == 21:
            print("\tKrupiér má blackjack, vítězí krupiér")
