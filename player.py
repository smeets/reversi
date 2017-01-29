import random

class Player:

	names = ["Max", "Oscar", "Bob", "Charles"]

	def __init__(self):
		self.name = random.choice(Player.names)

	def make_move(self, game):
		abstract

class RandomPlayer(Player):

	def next_move(self, game):
		return random.choice(game.legal_moves())

class MinMaxPlayer(Player):

	def next_move(self, game):
		return "1A"

class AlphaBetaPlayer(Player):

	def next_move(self, game):
		return "1A"