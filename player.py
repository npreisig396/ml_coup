class Player:
    def __init__(self, i, deck, ui, game=None):
        self.idx = i
        if deck:
            self.coins = 2
            self.cards = [deck.draw(), deck.draw()]
            self.ui = ui

    def give(self,card):
        self.cards.append(card)

    def get_action(self):
        a = self.ui.get_action()
        while not a.isdigit() or int(a) >= 7 or (int(a) == 3 and self.coins < 3) or (int(a) == 6 and self.coins < 7) or (int(a) != 6 and self.coins >= 10):
            a = self.ui.get_action()
        return int(a)

    def get_challenge(self):
        a = self.ui.get_challenge()
        while a not in 'YN':
            a = self.ui.get_challenge()
        return a

    def get_block(self):
        a = self.ui.get_block()
        while a not in 'YN':
            a = self.ui.get_block()
        return a

    def reveal_card(self,challenge=None):
        idx = self.ui.get_reveal()
        while not idx.isdigit() or int(idx) >= len(self.cards):
            idx = self.ui.get_reveal()
        return self.cards.pop(int(idx))
    
    def return_card(self):
        idx = self.ui.get_return()
        while not idx.isdigit() or int(idx) >= len(self.cards):
            idx = self.ui.get_return()
        return self.cards.pop(int(idx))

    def get_target(self, players):
        t = self.ui.get_target()
        while not t.isdigit() or int(t) >= len(players) or len(players[int(t)].cards) == 0 or int(t) == self.idx:
            t = self.ui.get_target()
        return int(t)

    def display(self,msg):
        self.ui.display(msg)

    def to_string(self):
         return f'Player {self.idx}, Coins: {self.coins}, Cards: {self.cards}'

    def close(self,winner):
        self.ui.close(winner)
