import random

class Player:
    def __init__(self,coins=2,cards=None):
        self.coins = coins
        self.cards = cards if cards else []

    def __str__(self):
        return '[' + str(self.cards) + ',' + str(self.coins) + ']'

class State:
    def __init__(self,game,idx,action=None,actioner=None):
        self.idx = idx
        self.my_coins = game.players[idx].coins
        self.my_cards = game.players[idx].cards
        self.coins = [player.coins for player in game.players]
        self.cards = [len(player.cards) for player in game.players]
        self.action = action
        self.actioner = actioner

    def get_actions(self):
        if self.my_coins < 3:
            return [0,1,2,4,5]
        elif self.my_coins < 7:
            return [0,1,2,3,4,5]
        elif self.my_coins >= 10:
            return [6]
        else:
            return [0,1,2,3,4,5,6]
        
    def get_targets(self):
        return [i for i in range(len(self.coins)) if i != self.idx and self.cards[i] > 0]

    def get_card_idx(self):
        return list(range(len(self.my_cards)))

    def __str__(self):
        s = f'\n\033[3mPlayer {self.idx}\'s turn\033[0m\n'
        for i in range(len(self.coins)):
            if i != self.idx:
                s += f'Player [{i}], Coins: {self.coins[i]}, Cards: {self.cards[i]}\n'
            else:
                s += f'\033[3mPlayer [{i}], Coins: {self.my_coins}, Cards: {self.my_cards}\033[0m\n'
        return s

class Deck:
    def __init__(self,cards=None):
        if cards:
            self.cards = cards
        else:
            self.cards = [
                    'Ambassador','Ambassador','Ambassador',
                    'Assassin','Assassin','Assassin',
                    'Captain','Captain','Captain',
                    'Contessa','Contessa','Contessa',
                    'Duke','Duke','Duke',
                    ]
            random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop(0)

    def replace(self,card):
        self.cards.append(card)
        random.shuffle(self.cards)
