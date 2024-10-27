# Výchozí balíček je definován v globálu/ jeho modifikaci pro speciální pravidla/testování?
# Fitness funkce/genetické programování nesmí vidět hodnoty karet, eliminovalo by to aspekt náhody
# Omezení dealera ( stát na 17, nebrat dál po převýšení hráčovy sumy?)
# Řešení probíhá pouze pro dvě karty, prokonzultovat se zbytkem jak to napojit na funkci která umožní další tah

import random
from random import randint

deck = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]

def setup():
    shuffle = random.randint(1,9)
    while shuffle > 0:
        random.shuffle(deck)
        shuffle -= 1
    asses()

def asses():
    player = 0
    dealer = 0
    acep = 0
    aced = 0
    print("Kontrola balíčku", deck)
    for i in range(0,2):
        player += deck[0]
        if deck[0] == 1:
            print("Hráč vytáhl eso")
            if player < 11:
                player += 10
                acep += 1
        if (player > 21) and (acep == 1):
            player -= 10
        del deck[0]
        dealer += deck[0]
        if deck[0] == 1:
            print("Krupiér vytáhl eso")
            if dealer < 11:
                dealer += 10
                aced +=1
        if (dealer > 21) and (aced == 1):
            dealer -= 10
        del deck[0]
    print("Hodnota hráčovy ruky je :", player)
    if player == 21:
        print("Hráč má blackjack, vítězí hráč")
    print("Hodnota krupiérovy ruky je:", dealer)
    if dealer == 21:
        print("Krupiér má blackjack, vítězí krupiér")

setup()