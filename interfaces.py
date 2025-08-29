import socket
import random

class Terminal:
    def __init__(self,rand=True,v=False):
        self.rand = rand
        self.v = v

    def get_action(self):
        if self.v:
            print('Select an action: ',end='')
        if self.rand:
            return str(random.randint(0,6))
        return input()

    def get_challenge(self):
        if self.v:
            print('Challenge? (Y/N): ',end='')
        if self.rand:
            return 'YN'[random.randint(0,1)]
        return input()

    def get_block(self):
        if self.v:
            print('Block? (Y/N): ',end='')
        if self.rand:
            return 'YN'[random.randint(0,1)]
        return input()

    def get_reveal(self,challenge=None):
        if self.v:
            print('Select a card to reveal: ',end='')
        if self.rand:
            return str(random.randint(0,2))
        return input()

    def get_return(self):
        if self.v:
            print('Select a card to return: ',end='')
        if self.rand:
            return str(random.randint(0,4))
        return input()

    def get_target(self):
        if self.v:
            print('Select a target: ',end='')
        if self.rand:
            return str(random.randint(0,3))
        return input()

    def display(self, msg):
        if self.v:
            print(msg)

    def close(self,winner):
        pass
