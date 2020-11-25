import numpy as np

class CheckersGame():

    def __init__(self, board, to_move, time_limit=None):
        self.board = np.copy(board)
        self.game_over = False # Maybe check this based on the board..?
        self.n_players = len(np.unique(board)) - 2
        self.player_turn = to_move
        # Should the board be a python list or a numpy array?
        # Numpy will probably be faster -- especially since during tree search we'll have to copy() it a lot.
        assert self.n_players in [2, 3, 4, 6]
        assert self.player_turn <= self.n_players

    @classmethod
    def new_game(cls, n_players, time_limit=None):
        # Initialize the board to the default state
        board = np.array(
                [[BOARD_INT_MAP[c] for c in r] for r in BOARD_STR.splitlines()],
            dtype=np.int8)
        # cls is basically going to be CheckersGame
        # so calling CheckersGame.new_game(n) is going to call CheckersGame(board, 0) down here
        return cls(board, 1, time_limit=time_limit)

    def move(self, move):
        # Given a move, (ie, a piece location and a destination)
        #  check if the specified piece belongs to the player whose turn it is
        #  check if the move is legal using pathfinding algorithm
        #  update the board to reflect the change
        #  check if this move causes the game to be over
        assert self.is_legal(move)
        pass

    def is_legal(self, move):
        # Check if a specified move is legal
        # This is separate from get_legal for speed
        return False

    def get_legal(self):
        # Return a list of legal moves for the moving player,
        # By graph exploration.
        return []

BOARD_STR = """\
....4............
....44...........
....444..........
....4444.........
3333ooooo5555....
.333oooooo555....
..33ooooooo55....
...3oooooooo5....
....ooooooooo....
....2oooooooo6...
....22ooooooo66..
....222oooooo666.
....2222ooooo6666
.........1111....
..........111....
...........11....
............1...."""
# I want to zero-index the players, but instead I'm going to make 0 be the empty space
BOARD_INT_MAP = {
    '.': -1, 'o': 0,
    '1': 1, '2': 2, '3': 3,
    '4': 4, '5': 5, '6': 6
}