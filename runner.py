import argparse
import time
import cProfile

from reversi import Reversi, move_repr, BLACK, WHITE
from agents import *

timeout = 60

parser = argparse.ArgumentParser(description="Play some Reversi.")
parser.add_argument("--verbose", help="output some helpful info", action="store_true")
parser.add_argument("--timeout", help="set the ai max turn time in seconds", action="store", type=int, dest="timeout", default=10)
parser.add_argument("--blind", help="silence board printing", action="store_true")
parser.add_argument("--profile", help="you know what is up", action="store_true")
parser.add_argument("--moves", help="print moves in YX format starting with player1", action="store_true")
parser.add_argument("--player1", choices=['rng', 'minmax', 'alphabeta', 'self'], help="specify player 1's agent")
parser.add_argument("--player2", choices=['rng', 'minmax', 'alphabeta', 'self'], help="specify player 2's agent")
# add --interactive option to step through each turn
args = parser.parse_args()

def play_game(game, agents):
    moves = []
    state = game.initial_state()
    if not args.blind:
       game.print_board(state)
    while True:
        passes = 0
        for agent in agents:
            # Press key to continue...
            time1 = time.time()
            if args.profile:
                pr = cProfile.Profile()
                pr.enable()
                move = agent.next_move(game, state, timeout)
                pr.disable()
                pr.print_stats(sort='time')
            else:
                move = agent.next_move(game, state, timeout)

            time2 = time.time()
            new_state = game.make_move(state, move)
            if args.verbose:
                print("Turn {} for player {} took {:0.3f} ms, {} score".format(state["turn"], state["player"], (time2-time1)*1000.0, game.score_player(new_state, state["player"])))
            state = new_state
            if not args.blind:
                game.print_board(state)
            if args.moves:
                print(move_repr(move))
            moves.append(move)
            if move == "pass":
                passes += 1
        if passes == len(agents):
            return state, moves

def str_to_agent(name):
    if name == "rng" or not name:
        return RandomAgent()
    elif name == "minmax":
        return MinMaxAgent()
    elif name == "alphabeta":
        return AlphaBetaAgent()
    elif name == "self":
        return InteractiveAgent()


game = Reversi()
agents = list(map(str_to_agent, [args.player1, args.player2]))

state, moves = play_game(game, agents)
winner, score = game.top_scoring_player(state)

#for move in moves:
#   print move_repr(move)

game.print_board(state)
print("Winner is {} at turn {} with {} score!".format(winner, state["turn"], score))
