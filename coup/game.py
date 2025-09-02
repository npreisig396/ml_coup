import random
from .interfaces import Terminal, Blank
from .utils import Deck, Player, State

def main():
    g = Game([Blank() for i in range(4)],verbose=True)
    g.play()

class Game:
    def __init__(self,interfaces,verbose=False):
        self.v = verbose
        self.interfaces = interfaces[:]
        random.shuffle(self.interfaces)
        self.idx = -1
        self.num_players = len(self.interfaces)
        self.players = [Player() for i in range(self.num_players)]
        self.is_over = False
        self.deck = Deck()
        self.actions = [self.income,self.foreign_aid,self.tax,self.assassinate,self.steal,self.exchange,self.coup]

    def play(self):
        if self.v:
            print('Starting Game')
        for player in self.players:
            player.cards.append(self.deck.draw())
            player.cards.append(self.deck.draw())

        while not self.is_over:
            self.next_turn()

        if self.v:
            print(self)
            print(f'Player {self.idx} wins!')

    def next_turn(self):
        idx = (self.idx + 1) % self.num_players
        while not self.players[idx].cards and idx != self.idx:
            idx = (idx + 1) % self.num_players
        if len([player for player in self.players if player.cards]) == 1:
            self.is_over = True
            self.idx = idx
        else:
            self.idx = idx
            if self.v:
                print(self)
            self.actions[self.interfaces[self.idx].get_action(State(self,self.idx))]()

    def offer_challenge(self,idx,msg,card,target=None):
        if self.players[idx].cards:
            if target != None:
                if self.interfaces[target].get_challenge(State(self,target)):
                    if self.v:
                        print(f'Player {target} is challenging')
                    return self.handle_challenge(idx,target,card)
                return 1
            else:
                i = (idx+1) % self.num_players
                while i != idx:
                    if self.players[i].cards and self.interfaces[i].get_challenge(State(self,i)):
                        if self.v:
                            print(f'Player {i} is challenging')
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
            if self.v:
                print(f'Player {challengee} revealed a {c} so player {challenger} loses a card')
            self.players[challengee].cards.append(self.deck.draw())
            c = self.players[challenger].cards.pop(self.interfaces[challenger].lose_influence(State(self,challenger)))
            self.deck.replace(c)
            if self.v:
                print(f'Player {challenger} revealed a {c}')
            return 1
        else:
            if self.v:
                print(f'Player {challengee} revealed a {c} so they lost a card')
            return 0

    def offer_block(self,idx,msg,card,target=None):
        if target != None:
            if self.interfaces[target].get_block(State(self,target),card):
                if self.v:
                    print(f'Player {target} is blocking with a {card}')
                return self.handle_block(idx,target,card)
            return 1
        else:
            i = (idx+1) % self.num_players
            while i != idx:
                if self.players[i].cards and self.interfaces[i].get_block(State(self,i),card):
                    if self.v:
                        print(f'Player {i} is blocking with a {card}')
                    return self.handle_block(idx,i,card)
                i = (i+1) % self.num_players
            return 1

    def handle_block(self,blockee,blocker,card):
        return 1-self.offer_challenge(blocker,f'Player {blocker} is blocking with {card}...',card,target=blockee)

    def income(self):
        if self.v:
            print(f'Player {self.idx} is taking income')
        self.players[self.idx].coins += 1

    def foreign_aid(self):
        if self.v:
            print(f'Player {self.idx} is taking foreign aid')
        if self.offer_block(self.idx,f'Player{self.idx} is taking foreign aid', 'Duke'):
            self.players[self.idx].coins += 2

    def tax(self):
        if self.v:
            print(f'Player {self.idx} is taxing')
        if self.offer_challenge(self.idx,f'Player{self.idx} is taxing...', 'Duke'):
            self.players[self.idx].coins += 3

    def assassinate(self): 
        self.players[self.idx].coins -= 3
        t = self.interfaces[self.idx].get_target(State(self,self.idx))
        if self.v:
            print(f'Player {self.idx} is assassinating player {t}')
        if self.offer_challenge(self.idx,f'Player{self.idx} is assassinating {t}', 'Assassin', target=t):
            if self.players[t].cards:
                if self.offer_block(self.idx,f'Player{self.idx} is assassinating {t}', 'Contessa', target=t):
                    if self.players[t].cards:
                        c = self.interfaces[t].lose_influence(State(self,t))
                        self.deck.replace(self.players[t].cards.pop(c))

    def steal(self):
        t = self.interfaces[self.idx].get_target(State(self,self.idx))
        if self.v:
            print(f'Player {self.idx} is stealing from player {t}')
        if self.offer_challenge(self.idx,f'Player{self.idx} is stealing from {t}...', 'Captain', target=t):
            if self.players[t].cards:
                if self.offer_block(self.idx,f'Player{self.idx} is stealing from {t}', 'Captain', target=t):
                    self.players[self.idx].coins += min(2,self.players[t].coins)
                    self.players[t].coins = max(0,self.players[t].coins-2)
                elif self.offer_block(self.idx,f'Player{self.idx} is stealing from {t}', 'Ambassador', target=t):
                    self.players[self.idx].coins += min(2,self.players[t].coins)
                    self.players[t].coins = max(0,self.players[t].coins-2)
            else:
                self.players[self.idx].coins += min(2,self.players[t].coins)
                self.players[t].coins = max(0,self.players[t].coins-2)


    def exchange(self):
        if self.v:
            print(f'Player {self.idx} is exchanging')
        if self.offer_challenge(self.idx,f'Player{self.idx} is exchanging...', 'Ambassador'):
            self.players[self.idx].cards.append(self.deck.draw())
            self.players[self.idx].cards.append(self.deck.draw())
            self.deck.replace(self.players[self.idx].cards.pop(self.interfaces[self.idx].replace_card(State(self,self.idx))))
            self.deck.replace(self.players[self.idx].cards.pop(self.interfaces[self.idx].replace_card(State(self,self.idx))))

    def coup(self):
        self.players[self.idx].coins -= 7
        t = self.interfaces[self.idx].get_target(State(self,self.idx))
        if self.v:
            print(f'Player {self.idx} is couping player {t}')
        c = self.interfaces[t].lose_influence(State(self,t))
        self.deck.replace(self.players[t].cards.pop(c))

    def __str__(self):
        s = f'\nPlayer {self.idx}\'s turn\n'
        for i in range(len(self.players)):
            s += f'Player [{i}], Coins: {self.players[i].coins}, Cards: {self.players[i].cards}\n'
        return s


if __name__ == '__main__':
    main()
