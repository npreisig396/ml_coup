import random
from coup.game import Game
from coup.utils import Player, Deck
from coup.interfaces import Terminal, Blank, Scripted

# deck = Deck(cards=[
#         'Ambassador','Ambassador','Ambassador',
#         'Assassin','Assassin','Assassin',
#         'Captain','Captain','Captain',
#         'Contessa','Contessa','Contessa',
#         'Duke','Duke','Duke',
#         ])

random.seed(0)

def run():
    # Game:
    #   - List of players
    #   - List of interfaces
    #   - Deck
    players = [Player(cards=['Captain']),Player(cards=['Ambassador'])]
    interfaces = [Scripted([4,1]),Scripted([0,0,0])]
    deck = Deck(cards=[
        'Ambassador','Ambassador',
        'Assassin','Assassin','Assassin',
        'Captain','Captain',
        'Contessa','Contessa','Contessa',
        'Duke','Duke','Duke',
        ])

    g = Game.from_state(players,interfaces,deck)
    g.next_turn()
    if players[0].coins != 4:
        return False
    if players[1].coins != 0:
        return False
    return 1
    


if __name__ == '__main__':
    main()
