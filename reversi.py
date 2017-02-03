from string import ascii_lowercase
import time
from operator import sub
import sys

EMPTY, BLACK, WHITE, BORDER = ' ', 'O', 'X', '#'

def move_repr(move):
    """ XY where X is row and Y is column, or PASS
    """
    if move == "pass":
        return "PASS"

    x, y = move
    repr = str(y)
    repr += ascii_lowercase[x-1]
    return repr

def opponent(state):
    return BLACK if state["player"] == WHITE else WHITE

def mark_line(board, player, src, dir, end):
    """ Change ownership of markers from src to end.
    """
    src += dir
    while src != end:
        board[src] = player
        src += dir

def raycast(state, src, dir):
    """ Shoot a ray from src in dir and see
        if current player has a mark with
        at least one enemy in between.
    """
    board = state["board"]
    loc = src + dir

    # Fail if surrounded by self
    if board[loc] == state["player"]:
        return None

    while board[loc] == opponent(state):
        loc += dir

    return loc if board[loc] == state["player"] else None

class Reversi:

    def __init__(self, h=8, w=8):
        self.h = h
        self.w = w
        self.h_ = h + 3
        self.w_ = w + 3

        # directions
        self.N, self.S = -self.w_, self.w_
        self.E, self.W = 1, -1
        self.NE = self.N + self.E
        self.NW = self.N + self.W
        self.SE = self.S + self.E
        self.SW = self.S + self.W
        self.directions = [self.W, self.E, self.N, self.S,
                           self.SW, self.SE, self.NW, self.NE]


    def initial_state(self):
        """ Black starts
        """
        center = self.map_2d(int(self.w_ / 2), int(self.h_ / 2))

        board = [BORDER if x % self.w_ == 0 and y % self.h_ == 0 else EMPTY
                 for x in range(self.w_)
                 for y in range(self.h_)]

        board[center], board[center + self.NW] = WHITE, WHITE
        board[center + self.W], board[center + self.N] = BLACK, BLACK

        return {"turn": 1, "player": BLACK, "board": board}

    def map_2d(self, x, y):
        return y * self.w_ + x

    def to_grid(self, move):
        """ Convert from (1, 1) to grid[0]
        """
        x,y = move
        return self.map_2d(x, y)

    def is_legal_move(self, state, move):
        """ Move is legal if player has marker in any
            direction with at least one enemy cell in
            between.
        """
        point = self.to_grid(move)

        if state["board"][point] != EMPTY:
            return None

        for dir in self.directions:
            if raycast(state, point, dir):
                return True

        return False

    def legal_moves(self, state):
        """ Expensive but simple
        """
        return [(x, y) for x in range(1, self.w)
                for y in range(1, self.h)
                if self.is_legal_move(state, (x, y))]

    def make_move(self, state, move):
        """ Returns next game state with move applied.
        """
        board = list(state["board"])

        if move != "pass":
            point = self.to_grid(move)
            player = state["player"]

            board[point] = state["player"]
            for dir in self.directions:
                end = raycast(state, point, dir)
                if end:
                    mark_line(board, player, point, dir, end)


        return {
            "turn": state["turn"] + 1,
            "player": opponent(state),
            "board": board
        }

    def over(self, state):
        """ Check if it's game over for current player.
        """
        return not self.legal_moves(state)


    def top_scoring_player(self, state):
        black = self.score_player(state, BLACK)
        white = self.score_player(state, WHITE)
        return (WHITE, white) if white > black else (BLACK, black)

    def print_board(self, state):
        """   a b c d e f g h
            1
            2
            3
            4       X O
            5       O X
            6
            7
            8
        """
        board = state["board"]

        def print_row(y):
            begin = y * (self.w_) + 1
            end = begin + self.w
            print('{} {}'.format(str(y), ' '.join(board[begin:end])))

        print("  {}".format(' '.join(ascii_lowercase[0:self.w])))

        for y in range(1, self.h+1):
            print_row(y)
            sys.stdout.flush()

    
    def score_player(self, state, player):
        """ Score(Player) = Sum(Markers for Player)
        """
        own = lambda mark: mark == player
        return len(list(filter(own, state["board"])))
    
