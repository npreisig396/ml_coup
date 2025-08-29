import random
from .utils import State

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
        pass
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
