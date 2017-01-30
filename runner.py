import argparse

from reversi import Reversi, move_repr, BLACK, WHITE
from agents import *

def play_game(game, agents):
    moves = []
    state = game.initial_state()
    while True:
        passes = 0
        for agent in agents:
            # Press key to continue...
            move = agent.next_move(game, state)
            state = game.make_move(state, move)
            moves.append(move)
            if game.over(state):
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

parser = argparse.ArgumentParser(description="Play some Reversi.")
parser.add_argument("--player1", choices=['rng', 'minmax', 'alphabeta'], help="specify player 1's agent")
parser.add_argument("--player2", choices=['rng', 'minmax', 'alphabeta'], help="specify player 2's agent")
# add --interactive option to step through each turn
args = parser.parse_args()

game = Reversi()
agents = list(map(str_to_agent, [args.player1, args.player2]))

state, moves = play_game(game, agents)
winner, score = game.top_scoring_player(state)

#for move in moves:
#   print move_repr(move)

game.print_board(state)
print("Winner is {} at turn {} with {} score!".format(winner, state["turn"], score))
