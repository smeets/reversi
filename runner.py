from reversi import Reversi
from player import *

def play_game(game, players):
	moves = []

	while True:
		for player in players:
			move = player.next_move(game)
			moves.append(move)
			game.make_move(move)
			if game.over():
				return player, moves

game = Reversi()
players = [RandomPlayer(), RandomPlayer()]

winner, moves = play_game(game, players)

print "Winner is", winner.name
print "Move list", moves