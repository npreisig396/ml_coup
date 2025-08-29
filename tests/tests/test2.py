import random
from coup.game import Game
from coup.utils import Player, Deck, State
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
    players = [Player(coins=3,cards=['Assassin']),Player(cards=['Contessa'])]
    interfaces = [Scripted([3,1,1,0]),Scripted([0,1,0])]
    # interfaces = [Terminal() for i in range(2)]
    deck = Deck(cards=['Captain'])

    g = Game.from_state(players,interfaces,deck)
    g.next_turn()
    if players[0].coins != 0:
        return False
    if players[0].cards != []:
        return False
    if players[1].cards != ['Captain']:
        return False
    return 1
    


if __name__ == '__main__':
    run()
