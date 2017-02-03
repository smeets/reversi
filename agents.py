import random
import time
from string import ascii_lowercase, index
from sys import version_info
from reversi import BLACK, WHITE

def opponent(player):
    return BLACK if player == WHITE else BLACK

py3 = version_info[0] > 2

def read_some_input(txt):
    if py3:
        return input(txt)
    else:
        return raw_input(txt)

class Agent:

    def next_move(self, game, state, timeout):
        abstract

    def legal_moves(self, game, state, max_player):
        tmp = state["player"]

        state["player"] = max_player
        max_moves = game.legal_moves(state)

        state["player"] = opponent(max_player)
        min_moves = game.legal_moves(state)

        state["player"] = tmp
        return max_moves, min_moves

class RandomAgent(Agent):

    def next_move(self, game, state, timeout):
        moves = game.legal_moves(state)
        return "pass" if not moves else random.choice(moves)

class InteractiveAgent(Agent):

    def next_move(self, game, state, timeout):
        """ Read 5d and convert to (5,4)
        """
        while True:
            action = read_some_input('What is your move? \n')
             # first char is row and is a number
            row = int(action[0])
            col = index(ascii_lowercase, action[1].lower()) + 1
            move = (col,row)
            if game.is_legal_move(state, move):
                return move
            else:
                print('{} is not a legal move!'.format(move))

class MinMaxAgent(Agent):
    """ A min-max searching agent.
    """
    def next_move(self, game, state, timeout):
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
        self.turn_timer = time.time() + timeout
        moves = game.legal_moves(state);
        if not moves:
            return "pass"
        else:
            depth = 4
            values = dict()
            for move in moves:
                if time.time() >= self.turn_timer:
                    break

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
                    if time.time() >= self.turn_timer:
                        break
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
                    if time.time() >= self.turn_timer:
                        break
                    temp_state = game.make_move(state, move)
                    value = self.max_val(game, temp_state, depth)
                    values[move] = value
                return values[min(values, key=values.get)]

    def heuristics(self, game, state):
        """ Returns number of marks for the agent
        """
        return game.score_player(state, self.player)


class AlphaBetaAgent(Agent):

    def next_move(self, game, state, timeout):
        # Very similar to minmax but do some magic with
        # inequalities so that we can prune states that
        # fail, or something...

        v = -100000
        a = -100000
        b = 100000

        self.player = state["player"]
        self.turn_time = time.time() + timeout
        moves = game.legal_moves(state);
        if not moves:
            return "pass"
        else:
            depth = 5
            best_value = -100000
            best_move = None
            for move in moves:
                if time.time() >= self.turn_time:
                    break
                temp_state = game.make_move(state, move)
                value = self.min_val(game, temp_state, depth, a, b)
                if(value > best_value):
                    best_value = value
                    best_move = move
                if(best_value > a):
                    a = best_value
            return best_move
        

    def max_val(self, game, state, depth, a, b):
        if depth == 0:
            max_moves, min_moves = self.legal_moves(game, state, self.player)
            return self.heuristics(game, state, max_moves, min_moves)
        else:
            moves = game.legal_moves(state);
            if not moves:
                max_moves, min_moves = self.legal_moves(game, state, self.player)
                return self.heuristics(game, state, max_moves, min_moves)
            else:
                depth -= 1
                best_value = -100000
                for move in moves:
                    if time.time() >= self.turn_time:
                        break
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
            max_moves, min_moves = self.legal_moves(game, state, self.player)
            return self.heuristics(game, state, max_moves, min_moves)
        else:
            moves = game.legal_moves(state);
            if not moves:
                max_moves, min_moves = self.legal_moves(game, state, self.player)
                return self.heuristics(game, state, max_moves, min_moves)
            else:
                depth -= 1
                best_value = 100000
                for move in moves:
                    if time.time() >= self.turn_time:
                        break
                    temp_state = game.make_move(state, move)
                    value = self.max_val(game, temp_state, depth, a, b)
                    if(value < best_value):
                        best_value = value
                    if(best_value >= a):
                        return best_value
                    if(best_value > b):
                        b = best_value
                return best_value

    def value(self, min_player_value, max_player_value):
        total = min_player_value + max_player_value
        if total != 0:
            return 100 * (max_player_value - min_player_value) / total
        else:
            return 0

    def coin_parity(self, game, state):
        max_coin = game.score_player(state, self.player)
        min_coin = game.score_player(state, opponent(self.player))
        return 100*(max_coin - min_coin)/(max_coin + min_coin)

#    def stability(self, game, state, max_moves, min_moves):
#        """ Stable, semi-stable and unstable coins """
#        min_player_stability = 0
#        max_player_stability = 0
#
#        for x in range(1, game.w):
#            for y in range(1, game.h):
#                point = game.map_2d(x, y)
#                owner = state["board"][point]
#                enemy = opponent(owner)
#                coin_stability = -1 # unstable
#
#                for dir in game.directions:
#                    hit = state["board"][point + dir]
#                    if hit == enemy:
#                        # Enemy found, we are now potentially flanked
#                        back = state["board"][point - dir]
#             
#
#                if owner == self.player:
#                    max_player_stability += coin_stability
#                else:
#                    min_player_stability += coin_stability
    
    def corners(self, game, state, max_moves, min_moves):
        """ Corner occupancy and closeness """
        top_left = (1, 1)
        top_right = (game.w, 1)
        bot_left = (1, game.h)
        bot_right = (game.w, game.h)
        corners = [top_left, top_right, bot_left, bot_right]
        enemy = opponent(self.player)

        min_player_corner = 0
        max_player_corner = 0

        # Corner occupancy
        for corner in corners:
            coin_owner = state["board"][game.to_grid(corner)]
            if coin_owner == self.player:
                max_player_corner += 25
            if coin_owner == enemy:
                min_player_corner += 25

        max_next_turn = lambda corner: 12.5 if corner in max_moves else 0
        min_next_turn = lambda corner: 12.5 if corner in min_moves else 0

        # Corner closeness/adjacency
        min_player_corner += sum(list(map(min_next_turn, corners)))
        max_player_corner += sum(list(map(min_next_turn, corners)))

        return self.value(min_player_corner, max_player_corner)
        

    def mobility(self, game, state, max_moves, min_moves):
        """ Actual mobility """
        min_player_mobility = len(min_moves)
        max_player_mobility = len(max_moves)
        return self.value(min_player_mobility, max_player_mobility)
    

    def heuristics(self, game, state, max_moves, min_moves):
        """ Returns number of marks for the agent
        """
        h_corners = self.corners(game, state, max_moves, min_moves) 
        h_mobility = self.mobility(game, state, max_moves, min_moves) 
        h_coins = self.coin_parity(game, state) 
        return h_corners * 800 + h_mobility * 80 + h_coins * 8
