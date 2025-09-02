import random

class Blank:
    def __init__(self):
        ...

    def get_action(self,state):
        return random.choice(state.get_actions())

    def get_target(self,state):
        return random.choice(state.get_targets())

    def lose_influence(self,state):
        return random.choice(state.get_card_idx())

    def get_challenge(self,state):
        return random.choice([1,0])

    def get_block(self,state,card):
        return random.choice([1,0])

    def replace_card(self,state):
        return random.choice(state.get_card_idx())

    def reveal_card(self,state):
        return random.choice(state.get_card_idx())
