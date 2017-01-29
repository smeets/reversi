import random

class Agent:

    def next_move(self, game, state):
        abstract

class RandomAgent(Agent):

    def next_move(self, game, state):
        moves = game.legal_moves(state)
        return "pass" if not moves else random.choice(moves)

class MinMaxAgent(Agent):

    def next_move(self, game, state):
        return (1, 1)

class AlphaBetaAgent(Agent):

    def next_move(self, game, state):
        return (1, 1)