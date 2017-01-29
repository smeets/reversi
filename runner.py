from reversi import Reversi, move_repr, BLACK, WHITE
from agents import RandomAgent

def play_game(game, agents):
	moves = []
	state = game.initial_state()
	while True:
		passes = 0
		for agent in agents:
			move = agent.next_move(game, state)
			state = game.make_move(state, move)
			moves.append(move)
			if game.over(state):
				passes += 1
		if passes == len(agents):
			return state, moves

game = Reversi()
agents = [RandomAgent(), RandomAgent()]

state, moves = play_game(game, agents)
winner, score = game.top_scoring_player(state)

#for move in moves:
#	print move_repr(move)

game.print_board(state)
print "Winner is", winner, "at turn", state["turn"], "with", score, "score!"