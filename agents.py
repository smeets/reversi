import random
import sys

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
        
        self.player = state["player"]
        moves = game.legal_moves(state);
        if not moves:
            return "pass"
        else:
            depth = 4
            values = dict()
            for move in moves:
                temp_state = game.make_move(state, move)
                value = self.min_val(game, temp_state, depth)
                values[move] = value
            return max(values, key=values.get)
        

    def max_val(self, game, state, depth):
        if depth == 0:
            return self.heuristics(game, state)
        else:
            moves = game.legal_moves(state);
            if not moves:
                return self.heuristics(game, state)
            else:
                depth -= 1
                values = dict()
                for move in moves:
                    temp_state = game.make_move(state, move)
                    value = self.min_val(game, temp_state, depth)
                    values[move] = value
                return values[max(values, key=values.get)]


    def min_val(self, game, state, depth):
        if depth == 0:
            return self.heuristics(game, state)
        else:
            moves = game.legal_moves(state);
            if not moves:
                return self.heuristics(game, state)
            else:
                depth -= 1
                values = dict()
                for move in moves:
                    temp_state = game.make_move(state, move)
                    value = self.max_val(game, temp_state, depth)
                    values[move] = value
                return values[min(values, key=values.get)]

    def heuristics(self, game, state):
        """ Returns number of marks for the agent
        """
        return game.score_player(state, self.player)


class AlphaBetaAgent(Agent):

    def next_move(self, game, state):
        # Very similar to minmax but do some magic with
        # inequalities so that we can prune states that
        # fail, or something...

        v = -sys.maxint - 1
        a = -sys.maxint - 1
        b = sys.maxint

        self.player = state["player"]
        moves = game.legal_moves(state);
        if not moves:
            return "pass"
        else:
            depth = 4
            values = dict()
            for move in moves:
                temp_state = game.make_move(state, move)
                value = self.min_val(game, temp_state, depth, a, b)
                values[move] = value
            return max(values, key=values.get)
        

    def max_val(self, game, state, depth, a, b):
        if depth == 0:
            return self.heuristics(game, state)
        else:
            moves = game.legal_moves(state);
            if not moves:
                return self.heuristics(game, state)
            else:
                depth -= 1
                best_value = -sys.maxint - 1
                for move in moves:
                    temp_state = game.make_move(state, move)
                    value = self.min_val(game, temp_state, depth, a, b)
                    if(value > best_value):
                        best_value = value
                    if(best_value >= b):
                        return best_value
                    if(best_value > a):
                        a = best_value
                return best_value


    def min_val(self, game, state, depth, a, b):
        if depth == 0:
            return self.heuristics(game, state)
        else:
            moves = game.legal_moves(state);
            if not moves:
                return self.heuristics(game, state)
            else:
                depth -= 1
                best_value = sys.maxint
                for move in moves:
                    temp_state = game.make_move(state, move)
                    value = self.max_val(game, temp_state, depth, a, b)
                    if(value < best_value):
                        best_value = value
                    if(best_value >= a):
                        return best_value
                    if(best_value > b):
                        b = best_value
                return best_value

    def heuristics(self, game, state):
        """ Returns number of marks for the agent
        """
        return game.score_player(state, self.player)