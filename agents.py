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
        
        moves = game.legal_moves(state);
        if not moves
            return "pass"
        else
            depth = 6
            values = dict()
            for move in moves:
                temp_state = game.make_move(state, move)
                value = min_val(self, game, temp_state, depth)
                values[move] = value
            return max(values, key=values.get)
        

    def max_val(self, game, state, depth):
        if depth = 0
            return heuristics()
        else
            moves = game.legal_moves(state);
            if not moves
                #We hit terminus
                #Return something
                #Win / loose
                #Or score?
            else 
                depth -= 1
                values = dict()
                for move in moves:
                    temp_state = game.make_move(state, move)
                    value = min_val(self, game, temp_state, depth)
                    values[move] = value
                return values[max(values, key=values.get)]


    def min_val(self, game, state, depth):
        if depth = 0
            return heuristics()
        else
            moves = game.legal_moves(state);
            if not moves
                #We hit terminus
                #Return something
                #Win / loose
                #Or score?
                return 0;
            else 
                depth -= 1
                values = dict()
                for move in moves:
                    temp_state = game.make_move(state, move)
                    value = max_val(self, game, temp_state, depth)
                    values[move] = value
                return values[min(values, key=values.get)]

    def heuristics(self, game, state):
        #return some kind of integer value
        return 0


class AlphaBetaAgent(Agent):

    def next_move(self, game, state):
        # Very similar to minmax but do some magic with
        # inequalities so that we can prune states that
        # fail, or something...
        return (1, 1)