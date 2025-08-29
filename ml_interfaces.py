import torch
import random
import torch.nn as nn
import torch.optim as optim

class Agent:
    def __init__(self,player,player_count=-1,game=None,rand=True):
        self.rand = rand
        self.player_count = player_count
        self.player = player
        self.game = game
        self.action_model = BaselineAction(game,player.idx)
        self.action_model.load_state_dict(torch.load('model.pth'))
        self.action_optimizer = optim.Adam(self.action_model.parameters(), lr = 0.01)
        self.choices = torch.zeros(0)

    def get_action(self):
        probs = self.action_model()
        p = 0
        idx = -1
        for i in range(len(probs)):
            if probs[i] > p:
                if (i != 3 and i != 6 and self.player.coins < 10) or (i == 3 and self.player.coins >= 3) or (i == 6 and self.player.coins >= 7):
                    p = probs[i]
                    idx = str(i)
        self.choices = torch.hstack((self.choices,p.log()))
        return idx
        
    def get_challenge(self):
        if self.rand:
            return 'YN'[random.randint(0,1)]
        return input()

    def get_block(self):
        if self.rand:
            return 'YN'[random.randint(0,1)]
        return input()

    def get_reveal(self,challenge=None):
        if self.rand:
            return str(random.randint(0,2))
        return input()

    def get_return(self):
        if self.rand:
            return str(random.randint(0,4))
        return input()

    def get_target(self):
        if self.rand:
            return str(random.randint(0,self.player_count-1))
        return input()

    def display(self, game):
        pass

    def close(self,winner):
        self.action_optimizer.zero_grad()
        reward = 1 if winner == self.player.idx else -1
        loss = 0
        for i in range(len(self.choices)):
            loss -= self.choices[-1-i] * reward
            reward *= .9
        loss.backward()
        self.action_optimizer.step()
        torch.save(self.action_model.state_dict(),'model.pth')

class BaselineAction(nn.Module):
    def __init__(self,game,idx):
        super(BaselineAction,self).__init__()
        self.idx = idx
        self.game = game
        self.mapping = {'Ambassador':0,'Assassin':1,'Captain':2,'Contessa':3,'Duke':4}

        self.model = nn.Sequential(
                nn.Linear(22,32),nn.ReLU(),
                nn.Linear(32,32),nn.ReLU(),
                nn.Linear(32,22),nn.ReLU(),
                nn.Linear(22,7),nn.Softmax(dim=0),
                )

    def forward(self):
        state = self.get_state()

        x = self.build_input(state)

        return self.model(x)

    def build_input(self,state):
        state = self.get_state()
        x = torch.zeros(4+5+5+4+4) # idx 1-hot, card1 1-hot, card2 1-hot, card counts, coin counts
        x[0] = self.idx
        if state[0] != 'None':
            x[1+self.mapping[state[0]]] = 1
        if state[1] != 'None':
            x[6+self.mapping[state[1]]] = 1
        for i in range(8):
            x[11+i] = state[2+i]
        return x

    def get_state(self):
        arr = []
        arr.append(self.game.players[self.idx].cards[0])
        arr.append(self.game.players[self.idx].cards[1] if len(self.game.players[self.idx].cards) == 2 else 'None')
        for player in self.game.players:
            arr.append(len(player.cards))
        for player in self.game.players:
            arr.append(player.coins)
        return arr
