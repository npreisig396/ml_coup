import random
from .interfaces import Terminal
from .utils import Deck, Player, State

def main():
    g = Game([Terminal(rand=False) for i in range(4)])
    g.play()

class Game:
    @classmethod
    def from_state(cls,players,interfaces,deck):
        g = cls(interfaces)
        g.players = players
        g.deck = deck
        g.is_over = False
        return g

    def __init__(self,interfaces):
        self.interfaces = interfaces
        self.num_players = len(self.interfaces)
        self.players = None
        self.deck = None
        self.idx = -1
        self.is_over = True
        self.actions = [self.income,self.foreign_aid,self.tax,self.assassinate,self.steal,self.exchange,self.coup]
        self.history = []

    def reset(self):
        random.shuffle(self.interfaces)
        self.players = [Player() for i in range(self.num_players)]
        self.is_over = False
        self.deck = Deck()
        
        for player in self.players:
            player.cards.append(self.deck.draw())
            player.cards.append(self.deck.draw())

    def play(self):
        self.reset()

        while not self.is_over:
            self.next_turn()

        for i in range(len(self.players)):
            self.interfaces[i].close(State(self,i))

    def next_turn(self):
        idx = (self.idx + 1) % self.num_players
        while not self.players[idx].cards and idx != self.idx:
            idx = (idx + 1) % self.num_players
        if len([player for player in self.players if player.cards]) == 1:
            self.is_over = True
        else:
            self.idx = idx
            self.actions[self.interfaces[self.idx].get_action(State(self,self.idx))]()

    def offer_challenge(self,idx,msg,card,target=None):
        if self.players[idx].cards:
            if target != None:
                if self.interfaces[target].get_challenge(State(self,target)):
                    return self.handle_challenge(idx,target,card)
                return 1
            else:
                i = (idx+1) % self.num_players
                while i != idx:
                    if self.players[i].cards and self.interfaces[i].get_challenge(State(self,i)):
                        return self.handle_challenge(idx,i,card)
                    i = (i+1) % self.num_players
                return 1
        else:
            return 1

    def handle_challenge(self,challengee,challenger,card):
        i = self.interfaces[challengee].reveal_card(State(self,challengee,card=card))
        c = self.players[challengee].cards.pop(i)
        self.deck.replace(c)
        if c == card:
            self.players[challengee].cards.append(self.deck.draw())
            if self.players[challenger].cards:
                c = self.interfaces[challenger].lose_influence(State(self,challenger))
                self.deck.replace(self.players[challenger].cards.pop(c))
            return 1
        else:
            return 0

    def offer_block(self,idx,msg,card,target=None):
        if target != None:
            if self.interfaces[target].get_block(State(self,target),card):
                return self.handle_block(idx,target,card)
            return 1
        else:
            i = (idx+1) % self.num_players
            while i != idx:
                if self.players[i].cards and self.interfaces[i].get_block(State(self,i),card):
                    return self.handle_block(idx,i,card)
                i = (i+1) % self.num_players
            return 1

    def handle_block(self,blockee,blocker,card):
        return 1-self.offer_challenge(blocker,f'Player {blocker} is blocking with {card}...',card,target=blockee)

    def income(self):
        self.history.append('Income')
        self.players[self.idx].coins += 1

    def foreign_aid(self):
        self.history.append('Foreign Aid')
        if self.offer_block(self.idx,f'Player{self.idx} is taking foreign aid', 'Duke'):
            self.players[self.idx].coins += 2

    def tax(self):
        self.history.append('Tax')
        if self.offer_challenge(self.idx,f'Player{self.idx} is taxing...', 'Duke'):
            self.players[self.idx].coins += 3

    def assassinate(self): 
        self.history.append('Assassinate')
        self.players[self.idx].coins -= 3
        t = self.interfaces[self.idx].get_target(State(self,self.idx))
        if self.offer_challenge(self.idx,f'Player{self.idx} is assassinating {t}', 'Assassin', target=t):
            if self.players[t].cards:
                if self.offer_block(self.idx,f'Player{self.idx} is assassinating {t}', 'Contessa', target=t):
                    if self.players[t].cards:
                        c = self.interfaces[t].lose_influence(State(self,t))
                        self.deck.replace(self.players[t].cards.pop(c))

    def steal(self):
        self.history.append('Steal')
        t = self.interfaces[self.idx].get_target(State(self,self.idx))
        if self.offer_challenge(self.idx,f'Player{self.idx} is stealing from {t}...', 'Captain', target=t):
            if self.players[self.idx].cards:
                if self.offer_block(self.idx,f'Player{self.idx} is stealing from {t}', 'Captain', target=t):
                    if self.players[self.idx].cards:
                        if self.offer_block(self.idx,f'Player{self.idx} is stealing from {t}', 'Ambassador', target=t):
                            self.players[self.idx].coins += min(2,self.players[t].coins)
                            self.players[t].coins = max(0,self.players[t].coins-2)

    def exchange(self):
        self.history.append('Exchange')
        if self.offer_challenge(self.idx,f'Player{self.idx} is exchanging...', 'Ambassador'):
            self.players[self.idx].cards.append(self.deck.draw())
            self.players[self.idx].cards.append(self.deck.draw())
            self.deck.replace(self.players[self.idx].cards.pop(self.interfaces[self.idx].replace_card(State(self,self.idx))))
            self.deck.replace(self.players[self.idx].cards.pop(self.interfaces[self.idx].replace_card(State(self,self.idx))))

    def coup(self):
        self.history.append('Coup')
        self.players[self.idx].coins -= 7
        t = self.interfaces[self.idx].get_target(State(self,self.idx))
        c = self.interfaces[t].lose_influence(State(self,t))
        self.deck.replace(self.players[t].cards.pop(c))

if __name__ == '__main__':
    main()
