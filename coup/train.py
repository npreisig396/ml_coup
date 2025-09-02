from .game import Game
from .interfaces import Terminal, Blank, Heuristic, Smart
from collections import defaultdict

def main():
    interfaces = [Terminal()] + [Smart(i) for i in range(3)]
    g = Game(interfaces)
    g.play()
    # sim(g,1000000)
   
def sim(g,n):
    import time
    s = time.perf_counter()

    cards = ['Ambassador','Assassin','Captain','Contessa','Duke']
    card_wins = defaultdict(int)
    interfaces = g.interfaces[:]

    for i in range(n):
        print(f'\r{i+1}/{n}, {[interface.wins for interface in interfaces]}',end='')
        g.reset()
        hands = [tuple(player.cards) for player in g.players]        
        while not g.is_over:
            g.next_turn()
        card_wins[hands[g.idx][0]] += 1
        if hands[g.idx][1] != hands[g.idx][0]:
            card_wins[hands[g.idx][1]] += 1
        for i in range(len(g.interfaces)):
            g.interfaces[i].close(i==g.idx)
    print(f'\nElapsed time: {time.perf_counter()-s:.6f} seconds')
    for card in cards:
        print(f'{card}: {card_wins[card]}')
    for interface in g.interfaces:
        print(type(interface), interface.wins)

if __name__ == '__main__':
    main()
