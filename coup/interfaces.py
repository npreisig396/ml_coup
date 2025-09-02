import random
from .utils import State
import torch
import torch.nn as nn
import torch.optim as optim

class Terminal:
    def __init__(self,verbose=True,rand=False):
        self.v = verbose
        self.r = rand

    def input(self,s,options):
        if self.v:
            print(s,end='')
        if self.r:
            a = str(options[random.randint(0,len(options)-1)])
        else:
            a = input()
        if self.v and self.r:
            print(a)
        return a

    def print(self,s):
        if self.v:
            print(s)

    def get_action(self,state):
        self.print(state)
        self.print(f'Player {state.idx}:')
        self.print('\t[0] Income')
        self.print('\t[1] Foreign Aid')
        self.print('\t[2] Tax')
        self.print('\t[3] Assassinate')
        self.print('\t[4] Steal')
        self.print('\t[5] Exchange')
        self.print('\t[6] Coup') 
        
        options = state.get_actions()
        a = self.input(f'Select an action from {options}: ', options)
        while not a.isdigit() or int(a) not in options:
            a = self.input(f'Select a valid action from {options}: ', options) 
        return int(a)

    def get_target(self,state):
        self.print(f'Player {state.idx}:')
        
        options = state.get_targets()
        t = self.input(f'Select a target from {state.get_targets()}: ',options)
        while not t.isdigit() or int(t) not in state.get_targets():
            t = self.input(f'Select a valid target from {state.get_targets()}: ',options)
        return int(t)
            
    def lose_influence(self,state):
        if len(state.my_cards) == 1:
            if self.v:
                print(f'Player {state.idx} is out!')
            return 0
        else:
            self.print(f'Player {state.idx}:')
            self.print(f'Cards: {state.my_cards}')
            options = state.get_card_idx()
            c = self.input(f'Select the index of the card you want to lose from {options}: ',options) 
            while not c.isdigit() or int(c) not in options:
                c = self.input(f'Select a valid index of a card you want to lose from {options}: ',options)
            return int(c) 

    def get_challenge(self,state):
        self.print(f'Player {state.idx}:')
        self.print(f'Cards: {state.my_cards}')
        a = self.input('Would you like to challenge? (Y/N): ',['Y','N']) 
        while a not in 'YN':
            a = self.input('Please enter Y or N: ',['Y','N']) 
        return 1 if a == 'Y' else 0

    def get_block(self,state,card):
        self.print(f'Player {state.idx}:')
        self.print(f'Cards: {state.my_cards}')
        a = self.input(f'Would you like to block with a {card}? (Y/N): ',['Y','N']) 
        while a not in 'YN':
            a = self.input('Please enter Y or N: ',['Y','N']) 
        return 1 if a == 'Y' else 0

    def replace_card(self,state):
        if len(state.my_cards) == 1:
            return 0
        else:
            self.print(f'Player {state.idx}:')
            self.print(f'Cards: {state.my_cards}')
            options = state.get_card_idx()
            c = self.input(f'Select the index of the card you want to return to the deck from {options}: ', options)
            while not c.isdigit() or int(c) not in options:
                c = self.input(f'Select a valid index of a card you want to return to the deck from {options}: ', options)
            return int(c)  

    def reveal_card(self,state):
        if len(state.my_cards) == 1:
            return 0
        else:
            self.print(f'Player {state.idx}:')
            self.print(f'Cards: {state.my_cards}')
            options = state.get_card_idx()
            c = self.input(f'Select the index of the card you want to reveal from {options}: ', options)
            while not c.isdigit() or int(c) not in options:
                c = self.input(f'Select a valid index of a card you want to reveal from {options}: ', options)
            return int(c)  

    def close(self,state):
        if state.my_cards and self.v:
            print(f'Player {state.idx} wins!')

class Blank:
    def __init__(self,verbose=False,random=False):
        self.v = verbose

    def get_action(self,state):
        return state.get_actions()[random.randint(0,len(state.get_actions())-1)]

    def get_target(self,state):
        return state.get_targets()[random.randint(0,len(state.get_targets())-1)]

    def lose_influence(self,state):
        return state.get_card_idx()[random.randint(0,len(state.get_card_idx())-1)]

    def get_challenge(self,state):
        return random.randint(0,1)

    def get_block(self,state,card):
        return random.randint(0,1)

    def reveal_card(self,state):
        return state.get_card_idx()[random.randint(0,len(state.get_card_idx())-1)]

    def replace_card(self,state):
        return state.get_card_idx()[random.randint(0,len(state.get_card_idx())-1)]

    def close(self,state):
        pass

class Heuristic:
    def __init__(self,verbose=False,random=False):
        self.v = verbose
        self.wins = 0

    def get_action(self,state):
        return state.get_actions()[random.randint(0,len(state.get_actions())-1)]

    def get_target(self,state):
        return state.get_targets()[random.randint(0,len(state.get_targets())-1)]

    def lose_influence(self,state):
        return state.get_card_idx()[random.randint(0,len(state.get_card_idx())-1)]

    def get_challenge(self,state):
        return random.randint(0,1)

    def get_block(self,state,card):
        if card in state.my_cards:
            return 1
        return random.randint(0,1)

    def reveal_card(self,state):
        if len(state.my_cards) == 1:
           return 0
        if state.my_cards[0] == state.should_reveal:
           return 0
        if state.my_cards[1] == state.should_reveal:
           return 1
        return state.get_card_idx()[random.randint(0,len(state.get_card_idx())-1)]

    def replace_card(self,state):
        return state.get_card_idx()[random.randint(0,len(state.get_card_idx())-1)]

    def close(self,state):
        if state:
            self.wins += 1

class Scripted:
    def __init__(self,script):
        self.script = script

    def get_action(self,state):
        return self.script.pop(0)

    def get_target(self,state):
        return self.script.pop(0)

    def lose_influence(self,state):
        return self.script.pop(0)

    def get_challenge(self,state):
        return self.script.pop(0)

    def get_block(self,state,card):
        return self.script.pop(0)

    def reveal_card(self,state):
        return self.script.pop(0)

    def replace_card(self,state):
        return self.script.pop(0)

    def close(self,state):
        pass

class Smart:
    def __init__(self,idx):
        self.action = nn.Sequential(nn.Linear(19,32),nn.ReLU(),nn.Linear(32,7),nn.Softmax(dim=0))
        self.action.load_state_dict(torch.load(f'models/action_only/model_{idx}.pth'))
        self.action_optimizer = optim.Adam(self.action.parameters(), lr = 0.01)
        self.mapping = {'Ambassador':0,'Assassin':1,'Captain':2,'Contessa':3,'Duke':4}
        self.choices = []
        self.wins = 0
        self.id = idx

    def get_action(self,state):
        x = torch.zeros(10 + 4 + 4 + 1)
        x[self.mapping[state.my_cards[0]]] = 1
        if len(state.my_cards) == 2:
            x[5+self.mapping[state.my_cards[1]]] = 1
        for i in range(4):
            x[10+i] = state.coins[i]
            x[14+i] = state.cards[i]
        x[18] = state.idx
        y = self.action(x)
    
        a = y[state.get_actions()].argmax()
        self.choices.append(y[a])
        return a

    def get_target(self,state):
        return state.get_targets()[random.randint(0,len(state.get_targets())-1)]

    def lose_influence(self,state):
        return state.get_card_idx()[random.randint(0,len(state.get_card_idx())-1)]

    def get_challenge(self,state):
        return random.randint(0,1)

    def get_block(self,state,card):
        return random.randint(0,1)

    def reveal_card(self,state):
        return state.get_card_idx()[random.randint(0,len(state.get_card_idx())-1)]

    def replace_card(self,state):
        return state.get_card_idx()[random.randint(0,len(state.get_card_idx())-1)]

    def close(self,state):
        self.action_optimizer.zero_grad()
        self.wins += 1 if state else 0
        reward = 1 if state else -1
        loss = 0
        for i in range(len(self.choices)):
            loss -= self.choices[-1-i] * reward
            reward *= .9
        if loss:
            loss.backward()
        self.action_optimizer.step()
        self.choices = []

        # torch.save(self.action.state_dict(),f'model_{self.id}.pth')
