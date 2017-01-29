class Reversi:

	def __init__(self, h=8, w=8):
		self.h = h
		self.w = w

	def legal_moves(self):
		return ["1A", "2A"]

	def make_move(self, move):
		pass

	def over(self):
		return True

	def display(self):
		print "reversi"
