import random
from .game import Game 
from .interfaces import Blank, Simple
from collections import defaultdict

def main():
    interfaces = [Simple() for i in range(4)]
    sim(interfaces,n=1) 

def sim(interfaces,n=1):
    import time
    s = time.perf_counter()
    wins = defaultdict(int)
    for i in range(n):
        print(f'{i}/{n}',end='\r')
        g = Game(interfaces,verbose=True)
        random.shuffle(g.interfaces)
        for player in g.players:
            player.cards.append(g.deck.draw())
            player.cards.append(g.deck.draw())
        while not g.is_over:
            g.next_turn()
        wins[g.interfaces[g.idx]] += 1 
        print('\n'.join([str(item) for item in g.history]))
    print(f'{n}/{n}')
    print(f'\nElapsed time: {time.perf_counter()-s:.6f} seconds')
    print([wins[i] for i in interfaces])

if __name__ == '__main__':
    main()
