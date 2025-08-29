from .game import Game
from .interfaces import Terminal, Blank, Heuristic
from collections import defaultdict

def main():
    interfaces = [Heuristic() for i in range(4)]
    g = Game(interfaces)
    sim(g,10000)
   
def sim(g,n):
    import time
    wins = [0]*4
    s = time.perf_counter()

    cards = ['Ambassador','Assassin','Captain','Contessa','Duke']
    card_wins = defaultdict(int)

    for i in range(n):
        print(f'\r{i+1}/{n}',end='')
        g.reset()
        hands = [tuple(player.cards) for player in g.players]        
        while not g.is_over:
            g.next_turn()
        card_wins[hands[g.idx][0]] += 1
        if hands[g.idx][1] != hands[g.idx][0]:
            card_wins[hands[g.idx][1]] += 1
    print(f'\nElapsed time: {time.perf_counter()-s:.6f} seconds')
    for card in cards:
        print(f'{card}: {card_wins[card]}')

if __name__ == '__main__':
    main()
