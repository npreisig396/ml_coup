import random

class Terminal:
    def __init__(self,rand=False):
        self.r = rand

    def get_action(self,state):
        print(state)
        print(f'Player {state.idx}:')
        print('\t[0] Income')
        print('\t[1] Foreign Aid')
        print('\t[2] Tax')
        print('\t[3] Assassinate')
        print('\t[4] Steal')
        print('\t[5] Exchange')
        print('\t[6] Coup') 
        
        options = state.get_actions()
        if self.r:
            a = random.choice(options)
            print(f'Select an action from {options}: {a}')
            return a
        else:
            a = input(f'Select an action from {options}: ')
            while not a.isdigit() or int(a) not in options:
                a = input(f'Select a valid action from {options}: ') 
            return int(a)

    def get_target(self,state):
        print(f'Player {state.idx}:')
        
        options = state.get_targets()
        if self.r:
            t = random.choice(options)
            print(f'Select a target from {state.get_targets()}: {t}')
            return t
        else:
            t = input(f'Select a target from {state.get_targets()}: ')
            while not t.isdigit() or int(t) not in state.get_targets():
                t = input(f'Select a valid target from {state.get_targets()}: ')
            return int(t)
            
    def lose_influence(self,state):
        if len(state.my_cards) == 1:
            return 0
        else:
            print(f'Player {state.idx}:')
            print(f'Cards: {state.my_cards}')
            options = state.get_card_idx()
            if self.r:
                c = random.choice(options)
                print(f'Select the index of the card you want to lose from {options}: {c}')
                return c
            else:
                c = input(f'Select the index of the card you want to lose from {options}: ') 
                while not c.isdigit() or int(c) not in options:
                    c = input(f'Select a valid index of a card you want to lose from {options}: ')
                return int(c) 

    def get_challenge(self,state):
        print(f'Player {state.idx}:')
        print(f'Cards: {state.my_cards}')
        if self.r:
            a = random.choice([1,0])
            p = 'Y' if a else 'N'
            print(f'Would you like to challenge? (Y/N): {p}')
            return a
        else:
            a = input('Would you like to challenge? (Y/N): ') 
            while a not in ['Y','N']:
                a = input('Please enter Y or N: ') 
            return 1 if a == 'Y' else 0

    def get_block(self,state,card):
        print(f'Player {state.idx}:')
        print(f'Cards: {state.my_cards}')
        if self.r:
            a = random.choice([1,0])
            p = 'Y' if a else 'N'
            print(f'Would you like to block with a {card}? (Y/N): {p}')
            return a
        else:
            a = input(f'Would you like to block with a {card}? (Y/N): ') 
            while a not in ['Y','N']:
                a = input('Please enter Y or N: ') 
            return 1 if a == 'Y' else 0

    def replace_card(self,state):
        if len(state.my_cards) == 1:
            return 0
        else:
            print(f'Player {state.idx}:')
            print(f'Cards: {state.my_cards}')
            options = state.get_card_idx()
            if self.r:
                c = random.choice(options)
                print(f'Select the index of the card you want to return to the deck from {options}: {c}')
                return c
            else:
                c = input(f'Select the index of the card you want to return to the deck from {options}: ')
                while not c.isdigit() or int(c) not in options:
                    c = input(f'Select a valid index of a card you want to return to the deck from {options}: ')
                return int(c)  

    def reveal_card(self,state):
        if len(state.my_cards) == 1:
            return 0
        else:
            print(f'Player {state.idx}:')
            print(f'Cards: {state.my_cards}')
            options = state.get_card_idx()
            if self.r:
                c = random.choice(options)
                print('Select the index of the card you want to reveal from {options}: {c}')
                return c
            else:
                c = input(f'Select the index of the card you want to reveal from {options}: ')
                while not c.isdigit() or int(c) not in options:
                    c = input(f'Select a valid index of a card you want to reveal from {options}: ')
                return int(c)
