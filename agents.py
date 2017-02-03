import random
import time
from string import ascii_lowercase, index
from sys import version_info, stdout
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
            #On some computers prining is optimized away, this row forced the print
            stdout.flush()
             # first char is row and is a number
            if (action == "pass"):
                return action
            row = int(action[0])
            col = index(ascii_lowercase, action[1].lower()) + 1
            move = (col,row)
            if game.is_legal_move(state, move):
                return move
            else:
                print('{} is not a legal move!'.format(move))
                stdout.flush()

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
        ranking = dict()
        self.prepare_ranking(ranking)
        self.player = state["player"]
        self.turn_time = time.time() + timeout
        moves = game.legal_moves(state);
        if not moves:
            return "pass"
        else:
            depth = 5
            best_value = -100000
            best_move = None
            ranked_moves = list()
            for move in moves:
                tup = (ranking[move],move)
                ranked_moves.append(tup)
            ranked_moves.sort(key=lambda tup: tup[0])
            for tup in ranked_moves:
                move = tup[1]
                if time.time() >= self.turn_time:
                    break
                temp_state = game.make_move(state, move)
                value = self.min_val(game, temp_state, depth, a, b, ranking)
                if(value > best_value):
                    best_value = value
                    best_move = move
                if(best_value > a):
                    a = best_value
            return best_move
        

    def max_val(self, game, state, depth, a, b, ranking):
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
                ranked_moves = list()
                for move in moves:
                    tup = (ranking[move],move)
                    ranked_moves.append(tup)
                ranked_moves.sort(key=lambda tup: tup[0])
                for tup in ranked_moves:
                    move = tup[1]
                    if time.time() >= self.turn_time:
                        break
                    temp_state = game.make_move(state, move)
                    value = self.min_val(game, temp_state, depth, a, b, ranking)
                    if(value > best_value):
                        best_value = value
                    if(best_value >= b):
                        return best_value
                    if(best_value > a):
                        a = best_value
                return best_value


    def min_val(self, game, state, depth, a, b, ranking):
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
                ranked_moves = list()
                for move in moves:
                    tup = (ranking[move],move)
                    ranked_moves.append(tup)
                ranked_moves.sort(key=lambda tup: tup[0])
                for tup in ranked_moves:
                    move = tup[1]
                    if time.time() >= self.turn_time:
                        break
                    temp_state = game.make_move(state, move)
                    value = self.max_val(game, temp_state, depth, a, b, ranking)
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

    def corner_closeness(self, game, state):
        player_closeness = 0
        enemy_closeness = 0
        temp_player = 0
        temp_enemy = 0
        corner = (1,1)
        first = (1,2)
        second = (2,1)
        third = (2,2)
        temp_player, temp_enemy = self.calc_corner_closeness(game, state, corner, first, second, third)
        player_closeness += temp_player
        enemy_closeness += temp_enemy
        corner = (1,9)
        first = (1,8)
        second = (2,9)
        third = (2,8)
        temp_player, temp_enemy = self.calc_corner_closeness(game, state, corner, first, second, third)
        player_closeness += temp_player
        enemy_closeness += temp_enemy
        corner = (9,1)
        first = (9,2)
        second = (8,1)
        third = (8,2)
        temp_player, temp_enemy = self.calc_corner_closeness(game, state, corner, first, second, third)
        player_closeness += temp_player
        enemy_closeness += temp_enemy
        corner = (9,9)
        first = (9,8)
        second = (8,9)
        third = (8,8)
        temp_player, temp_enemy = self.calc_corner_closeness(game, state, corner, first, second, third)
        player_closeness += temp_player
        enemy_closeness += temp_enemy
        return -12.5 * (player_closeness - enemy_closeness);

    def calc_corner_closeness(self, game, state, corner, first, second, third):
        enemy = opponent(self.player)
        player_closeness = 0
        enemy_closeness = 0
        if (state["board"][game.to_grid(corner)]) == ' ':
            if (state["board"][game.to_grid(first)]) == self.player: player_closeness += 1
            elif (state["board"][game.to_grid(first)]) == enemy: enemy_closeness += 1
            if(state["board"][game.to_grid(second)]) == self.player: player_closeness += 1
            elif (state["board"][game.to_grid(second)]) == enemy: enemy_closeness += 1
            if(state["board"][game.to_grid(third)]) == self.player: player_closeness += 1
            elif (state["board"][game.to_grid(third)]) == enemy: enemy_closeness += 1
        return player_closeness, enemy_closeness

    def heuristics(self, game, state, max_moves, min_moves):
        """ Returns number of marks for the agent
        """
        h_corners = self.corners(game, state, max_moves, min_moves) 
        h_mobility = self.mobility(game, state, max_moves, min_moves) 
        h_coins = self.coin_parity(game, state) 
        h_closeness = self.corner_closeness(game, state)
        return h_corners * 800 + h_closeness * 400 + h_mobility * 80 + h_coins * 8

    def prepare_ranking(self, ranking):
        #Used to rank moves for better alpha beta pruning
        ranking[(1,1)] = 4
        ranking[(1,2)] = -3
        ranking[(1,3)] = 2
        ranking[(1,4)] = 2
        ranking[(1,5)] = 2
        ranking[(1,6)] = 2
        ranking[(1,7)] = -3
        ranking[(1,8)] = 4
        ranking[(2,1)] = -3
        ranking[(2,2)] = -4
        ranking[(2,3)] = -1
        ranking[(2,4)] = -1
        ranking[(2,5)] = -1
        ranking[(2,6)] = -1
        ranking[(2,7)] = -4
        ranking[(2,8)] = -3
        ranking[(3,1)] = 2
        ranking[(3,2)] = -1
        ranking[(3,3)] = 1
        ranking[(3,4)] = 0
        ranking[(3,5)] = 0
        ranking[(3,6)] = 1
        ranking[(3,7)] = -1
        ranking[(3,8)] = 2
        ranking[(4,1)] = 2
        ranking[(4,2)] = -1
        ranking[(4,3)] = 0
        ranking[(4,4)] = 1
        ranking[(4,5)] = 1
        ranking[(4,6)] = 0
        ranking[(4,7)] = -1
        ranking[(4,8)] = 2
        ranking[(5,1)] = 2
        ranking[(5,2)] = -1
        ranking[(5,3)] = 0
        ranking[(5,4)] = 1
        ranking[(5,5)] = 1
        ranking[(5,6)] = 0
        ranking[(5,7)] = -1
        ranking[(5,8)] = 2
        ranking[(6,1)] = 2
        ranking[(6,2)] = -1
        ranking[(6,3)] = 1
        ranking[(6,4)] = 0
        ranking[(6,5)] = 0
        ranking[(6,6)] = 1
        ranking[(6,7)] = -1
        ranking[(6,8)] = 2
        ranking[(7,1)] = -3
        ranking[(7,2)] = -4
        ranking[(7,3)] = -1
        ranking[(7,4)] = -1
        ranking[(7,5)] = -1
        ranking[(7,6)] = -1
        ranking[(7,7)] = -4
        ranking[(7,8)] = -3
        ranking[(8,1)] = 4
        ranking[(8,2)] = -3
        ranking[(8,3)] = 2
        ranking[(8,4)] = 2
        ranking[(8,5)] = 2
        ranking[(8,6)] = 2
        ranking[(8,7)] = -3
        ranking[(8,8)] = 4
