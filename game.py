class CheckersGame():

    def __init__(self, board, to_move):
        self.board = []
        self.game_over = False
        self.n_players = # number of unique values in board
        self.player_turn = to_move
        # Should the board be a python list or a numpy array?
        # Numpy will probably be faster -- especially since during tree search we'll have to copy() it a lot.
        assert n_players % 2 == 0
        assert player_turn < n_players

    @classmethod
    def new_game(cls, n_players):
        # Initialize the board to the default state
        # ie, distribute the 
        assert n_players % 2 == 0
        board = []...
        # cls is basically going to be CheckersGame
        # so calling CheckersGame.new_game(n) is going to call CheckersGame(board, 0) down here
        return cls(board, 0)

    def move(self, move):
        # Given a move, (ie, a piece location and a destination)
        #  check if the specified piece belongs to the player whose turn it is
        #  check if the move is legal using pathfinding algorithm
        #  update the board to reflect the change
        #  check if this move causes the game to be over
        pass

    def is_legal(self, move):
        # Check if a specified move is legal
        # This is separate from get_legal for speed
        return False

    def get_legal(self):
        # Return a list of legal moves for the moving player.
        return []
