import random
from player import Player
from interfaces import Terminal

class Game:
    def __init__(self, interfaces):
        self.deck = Deck()
        self.num_players = len(interfaces)
        self.players = [Player(i,self.deck,interfaces[i],game=self) for i in range(len(interfaces))]
        self.current_player = -1
        self.is_over = False
        self.actions = [
                self.income,self.foreign_aid,self.tax,
                self.assassinate,self.steal,self.exchange,
                self.coup
                ]

    def next_turn(self):
        next_player = (self.current_player+1) % self.num_players
        while len(self.players[next_player].cards) == 0:
            next_player = (next_player+1) % self.num_players
        self.current_player = next_player

        for player in self.players:
            if len(player.cards) > 0:
                if self.is_over:
                    self.is_over = False
                    break
                self.is_over = True
        if self.is_over:
            self.broadcast(f'Player {self.current_player} has won!')
            for player in self.players:
                player.close(winner=self.current_player)
            return

        self.broadcast(self.to_string())
        action = self.players[self.current_player].get_action()
        self.actions[action]()

    def broadcast(self,msg,speaker=None):
        for player in self.players:
            if player.idx != speaker:
                player.display(msg)

    def to_string(self):
        return ('-'*50) + f'\nPlayer {self.current_player}\'s turn\n' + '\n'.join([player.to_string() for player in self.players])

    def handle_challenge(self,card,target=None):
        if target != None:
            if self.players[target].get_challenge() == 'Y':
                self.broadcast(f'Player {target} is challenging', speaker=target)
                if self.challenge_action(card) == 0:
                    self.broadcast(f'Player {self.current_player} was telling the truth!', speaker=self.current_player)
                    self.deck.replace(self.players[target].reveal_card())
                    return 2
                else:
                    self.broadcast(f'Player {self.current_player} was lying!',speaker=self.current_player)
                    return 0
        else:
            idx = (self.current_player+1) % self.num_players
            while idx != self.current_player:
                if len(self.players[idx].cards) > 0 and self.players[idx].get_challenge() == 'Y':
                    self.broadcast(f'Player {idx} is challenging', speaker=idx)
                    if self.challenge_action(card) == 0:
                        self.deck.replace(self.players[idx].reveal_card())
                        self.broadcast(f'Player {self.current_player} was telling the truth!', speaker=self.current_player)
                        return 2
                    else:
                        self.broadcast(f'Player {self.current_player} was lying!',speaker=self.current_player)
                        return 0
                idx = (idx+1) % self.num_players
        return 1

    def challenge_action(self,card):
        r = self.players[self.current_player].reveal_card(challenge=[card])
        self.deck.replace(r)
        if card == r:
            self.players[self.current_player].give(self.deck.draw())
            return 0
        return 1

    def handle_block(self,cards,target=None):
        if target != None:
            if self.players[target].get_block() == 'Y':
                self.broadcast(f'Player {target} is blocking',speaker=target)
                if self.players[self.current_player].get_challenge() == 'Y':
                    self.broadcast(f'Player {self.current_player} is challenging',speaker=self.current_player)
                    if self.challenge_block(cards,target) == 0:
                        self.deck.replace(self.players[self.current_player].reveal_card())
                        self.broadcast(f'Player {target} was telling the truth!', speaker=target)
                        return 0
                    else:
                        self.broadcast(f'Player {target} was lying!', speaker=target)
                        return 1
                    return 0
        else:
            idx = (self.current_player+1) % self.num_players
            while idx != self.current_player:
                if len(self.players[idx].cards) > 0 and self.players[idx].get_block() == 'Y':
                    self.broadcast(f'Player {idx} is blocking',speaker=idx)
                    if self.players[self.current_player].get_challenge() == 'Y':
                        self.broadcast(f'Player {self.current_player} is challenging',speaker=self.current_player)
                        if self.challenge_block(cards,idx) == 0:
                            self.deck.replace(self.players[self.current_player].reveal_card())
                            self.broadcast(f'Player {idx} was telling the truth!', speaker=idx)
                            return 0
                        else:
                            self.broadcast(f'Player {idx} was lying!', speaker=idx)
                            return 1
                    return 0
                idx = (idx+1) % self.num_players
        return 1

    def challenge_block(self,cards,idx):
        r = self.players[idx].reveal_card(challenge=cards) 
        self.deck.replace(r)
        if r in cards:
            self.players[idx].give(self.deck.draw())
            return 0
        return 1

    def income(self):
        self.broadcast(f'Player {self.current_player} is taking income')
        self.players[self.current_player].coins += 1

    def foreign_aid(self):
        self.broadcast(f'Player {self.current_player} is taking foreign aid')
        if self.handle_block(['Duke']):
            self.players[self.current_player].coins += 2

    def tax(self):
        self.broadcast(f'Player {self.current_player} is taxing')
        if self.handle_challenge('Duke'):
            self.players[self.current_player].coins += 3

    def assassinate(self):
        self.players[self.current_player].coins -= 3
        t = self.players[self.current_player].get_target(self.players)
        self.broadcast(f'Player {self.current_player} is assassinating player {t}')
        ch = self.handle_challenge('Assassin',target=t)
        if ch == 2:
            if self.players[t].cards:
                self.deck.replace(self.players[t].reveal_card())
        elif ch == 1 and self.handle_block(['Contessa'],target=t):
            if self.players[t].cards:
                self.deck.replace(self.players[t].reveal_card())

    def steal(self):
        t = self.players[self.current_player].get_target(self.players)
        self.broadcast(f'Player {self.current_player} is stealing from {t}')
        ch = self.handle_challenge('Captain',target=t)
        if ch == 2:
            self.players[self.current_player].coins += min(self.players[t].coins,2)
            self.players[t].coins = max(self.players[t].coins-2,0)
        elif ch == 1 and self.handle_block(['Captain','Ambassador'],target=t):
            self.players[self.current_player].coins += min(self.players[t].coins,2)
            self.players[t].coins = max(self.players[t].coins-2,0)

    def exchange(self):
        self.broadcast(f'Player {self.current_player} is exchanging')
        if self.handle_challenge('Ambassador'):
            self.players[self.current_player].give(self.deck.draw())
            self.players[self.current_player].give(self.deck.draw())

            self.deck.replace(self.players[self.current_player].return_card())
            self.deck.replace(self.players[self.current_player].return_card())

    def coup(self):
        self.players[self.current_player].coins -= 7
        t = self.players[self.current_player].get_target(self.players)
        self.broadcast(f'Player {self.current_player} is couping player {t}')
        self.deck.replace(self.players[t].reveal_card())

    def get_state(self,idx):
        arr = [idx]
        arr.append(self.players[idx].cards[0])
        arr.append(self.players[idx].cards[1] if len(self.players[idx].cards) == 2 else 0)
        for player in self.players:
            arr.append(len(player.cards))
        for player in self.players:
            arr.append(player.coins)


class Deck:
    def __init__(self):
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

if __name__ == '__main__':
    interfaces = [Terminal(v=True) for i in range(4)]
    g = Game(interfaces)

    while not g.is_over:
        g.next_turn()
