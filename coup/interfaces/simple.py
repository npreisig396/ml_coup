import torch
import torch.nn as nn
import random

class Simple:
    def __init__(self):
        self.mapping = {'Ambassador': 0,'Assassin':1,'Captain':2,'Contessa':3,'Duke':4}

        self.actions = nn.Linear(1 + 10 + 4 + 4, 7)
        self.target = nn.Linear(1 + 10 + 4 + 4 + 5, 4)
        self.lose = nn.Linear(1 + 10 + 4 + 4, 2)
        self.challenge = nn.Linear(1 + 10 + 4 + 4 + 5 + 4, 2)
        self.block = nn.Linear(1 + 10 + 4 + 4 + 5 + 4, 2)
        self.replace = nn.Linear(1 + 20 + 4 + 4, 4)
        self.reveal = nn.Linear(1 + 10 + 4 + 4, 2)

        self.choices = []

    def get_action(self,state):
        x = torch.zeros(19)
        x[0] = state.idx
        x[1+self.mapping[state.my_cards[0]]] = 1
        if len(state.my_cards) > 1:
            x[6+self.mapping[state.my_cards[1]]] = 1
        for i in range(4):
            x[11+i] = state.coins[i]
            x[15+i] = state.cards[i]
        probs = self.actions(x).softmax(dim=0)
        mask = torch.tensor([1 if i in state.get_actions() else 0 for i in range(7)])
        choice = (probs * mask).argmax()
        self.choices.append(probs[choice])
        return choice

    def get_target(self,state):
        x = torch.zeros(24)
        x[0] = state.idx
        x[1+self.mapping[state.my_cards[0]]] = 1
        if len(state.my_cards) > 1:
            x[6+self.mapping[state.my_cards[1]]] = 1
        for i in range(4):
            x[11+i] = state.coins[i]
            x[15+i] = state.cards[i]
        if state.action:
            x[19+self.mapping[state.action]] = 1
        probs = self.target(x).softmax(dim=0)
        mask = torch.tensor([1 if i in state.get_targets() else 0 for i in range(4)])
        choice = (probs * mask).argmax()
        self.choices.append(probs[choice])
        return choice

    def lose_influence(self,state):
        x = torch.zeros(19)
        x[0] = state.idx
        x[1+self.mapping[state.my_cards[0]]] = 1
        if len(state.my_cards) > 1:
            x[6+self.mapping[state.my_cards[1]]] = 1
        for i in range(4):
            x[11+i] = state.coins[i]
            x[15+i] = state.cards[i]
        probs = self.lose(x).softmax(dim=0)
        mask = torch.tensor([1 if i in state.get_card_idx() else 0 for i in range(2)])
        choice = (probs * mask).argmax()
        self.choices.append(probs[choice])
        return choice

    def get_challenge(self,state):
        x = torch.zeros(28)
        x[0] = state.idx
        x[1+self.mapping[state.my_cards[0]]] = 1
        if len(state.my_cards) > 1:
            x[6+self.mapping[state.my_cards[1]]] = 1
        for i in range(4):
            x[11+i] = state.coins[i]
            x[15+i] = state.cards[i]
        x[19+self.mapping[state.action]] = 1
        x[24+state.actioner] = 1
        probs = self.challenge(x).softmax(dim=0)
        choice = probs.argmax()
        self.choices.append(probs[choice])
        return choice

    def get_block(self,state):
        x = torch.zeros(28)
        x[0] = state.idx
        x[1+self.mapping[state.my_cards[0]]] = 1
        if len(state.my_cards) > 1:
            x[6+self.mapping[state.my_cards[1]]] = 1
        for i in range(4):
            x[11+i] = state.coins[i]
            x[15+i] = state.cards[i]
        x[19+self.mapping[state.action]] = 1
        x[24+state.actioner] = 1
        probs = self.block(x).softmax(dim=0)
        choice = probs.argmax()
        self.choices.append(probs[choice])
        return choice

    def replace_card(self,state):
        x = torch.zeros(29)
        x[0] = state.idx
        x[1+self.mapping[state.my_cards[0]]] = 1
        if len(state.my_cards) > 1:
            x[6+self.mapping[state.my_cards[1]]] = 1
        if len(state.my_cards) > 2:
            x[11+self.mapping[state.my_cards[2]]] = 1
        if len(state.my_cards) > 3:
            x[16+self.mapping[state.my_cards[3]]] = 1
        for i in range(4):
            x[21+i] = state.coins[i]
            x[25+i] = state.cards[i]
        probs = self.replace(x).softmax(dim=0)
        mask = torch.tensor([1 if i in state.get_card_idx() else 0 for i in range(4)])
        choice = (probs * mask).argmax()
        self.choices.append(probs[choice])
        return choice

    def reveal_card(self,state):
        x = torch.zeros(19)
        x[0] = state.idx
        x[1+self.mapping[state.my_cards[0]]] = 1
        if len(state.my_cards) > 1:
            x[6+self.mapping[state.my_cards[1]]] = 1
        for i in range(4):
            x[11+i] = state.coins[i]
            x[15+i] = state.cards[i]
        probs = self.reveal(x).softmax(dim=0)
        mask = torch.tensor([1 if i in state.get_card_idx() else 0 for i in range(2)])
        choice = (probs * mask).argmax()
        self.choices.append(probs[choice])
        return choice
