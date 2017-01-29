from reversi import Reversi
from player import *

def play_game(game, players):
	moves = []
	state = game.initial_state()
	while True:
		for player in players:
			move = player.next_move(game, state)
			moves.append(move)
			state = game.make_move(state, move)
			if game.over(state):
				return player, state, moves

game = Reversi()
players = [RandomPlayer(), RandomPlayer()]

winner, state, moves = play_game(game, players)

print "Winner is", winner.name
print "Move list", moves
game.display(state)