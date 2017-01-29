import random

class Player:

	names = ["Max", "Oscar", "Bob", "Charles"]

	def __init__(self):
		self.name = random.choice(Player.names)

	def next_move(self, game, state):
		abstract

class RandomPlayer(Player):

	def next_move(self, game, state):
		return random.choice(game.legal_moves(state))

class MinMaxPlayer(Player):

	def next_move(self, game, state):
		return (1, 1)

class AlphaBetaPlayer(Player):

	def next_move(self, game, state):
		return (1, 1)