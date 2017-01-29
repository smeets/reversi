from string import ascii_lowercase
from operator import sub

class Reversi:

	def __init__(self, h=8, w=8):
		self.h = h
		self.w = w

	def initial_state(self):
		cx = self.h / 2
		cy = self.w / 2

		board = self.make_board()
		board[self.map_2d(cx, cy)] = "X"
		board[self.map_2d(cx - 1, cy)] = "O"
		board[self.map_2d(cx - 1, cy - 1)] = "X"
		board[self.map_2d(cx, cy - 1)] = "O"

		return {"turn": 0, "player": "O", "board": board}

	def map_2d(self, x, y):
		return y * self.w + x

	def legal_moves(self, state):
		return [(1, 1), (2, 2)]

	def make_move(self, state, move):
		return state

	def over(self, state):
		return True

	def display(self, state):

		board = state["board"]

		def print_row(y):
			row = [str(y + 1)]
			for x in xrange(self.w):
				row.append(board[y * self.w + x])
			print ' '.join(row)

		print " ", ' '.join([ascii_lowercase[i] for i in range(self.w)])
		for y in xrange(self.h):
			print_row(y)

	def make_board(self):
		return [" " for x in range(1, self.w + 1)
				for y in range(1, self.h + 1)]