import random

class Agent:

    def next_move(self, game, state):
        abstract

class RandomAgent(Agent):

    def next_move(self, game, state):
        moves = game.legal_moves(state)
        return "pass" if not moves else random.choice(moves)

class MinMaxAgent(Agent):
    """ A min-max searching agent.
    """
    def next_move(self, game, state):
        # Idea is to go search in tree successors(state)
        # and select move that leads to best outcome.
        #
        # E.g.: argmax(search(successors(state)))
        #
        # successors(state) should be a list of (move, state)
        # then we can recursively descend search the tree and
        # propagate min-max values upwards so that we finally
        # can select the best move.
        return (1, 1)

class AlphaBetaAgent(Agent):

    def next_move(self, game, state):
        # Very similar to minmax but do some magic with
        # inequalities so that we can prune states that
        # fail, or something...
        return (1, 1)