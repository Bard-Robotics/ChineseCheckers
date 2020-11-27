import numpy as np

class CheckersGame():
    
    PLAYER_COLOR = {
        2: [1, 4],
        3: [1, 3, 5],
        4: [1, 3, 4, 6],
        6: [1, 2, 3, 4, 5, 6]
    }
    def __init__(self, board, to_move):
        # The board is a numpy array so that we can copy it really fast
        self._board = np.copy(board)
        self.winner = None
        self.n_players = len(np.unique(board)) - 2
        self.colors = CheckersGame.PLAYER_COLOR[self.n_players]
        self.player_turn = to_move
        assert self.n_players in [2, 3, 4, 6]
        assert 0 <= self.player_turn < self.n_players

    @staticmethod
    def opposite(color):
        return (color + 2) % 6 + 1

    @classmethod
    def new_game(cls, n_players):
        # All we're doing here is taking the default board and removing the tokens of players who aren't playing
        colors = cls.PLAYER_COLOR[n_players]
        remove_tokens = np.vectorize(lambda i: i if i in colors or i <= 0 else 0)
        board = remove_tokens(FULL_BOARD)
        # cls is basically going to be CheckersGame
        # so calling CheckersGame.new_game(n) is going to call CheckersGame(board, 0) down here
        return cls(board, 0)

    def move(self, start, end):
        # Given a move, (ie, a piece location and a destination)
        #  check if the specified piece belongs to the player whose turn it is
        #  check if the move is legal using pathfinding algorithm
        #  update the board to reflect the change
        #  check if this move causes the game to be over
        assert self.is_legal(start, end)
        assert self._board[start] == self.colors[self.player_turn]
        assert self.winner is None
       
        # Move pieces
        self._board[end] = self._board[start]
        self._board[start] = 0

        # Check the winner
        # Is the destination in a home zone?
        if (FULL_BOARD[end] > 0
            # Is the home zone full?
            and all(self._board[i] > 0 for i in START_ZONES[FULL_BOARD[end]])
            # Is that home zone a goal zone for a color that's in the game?
            and self.opposite(FULL_BOARD[end]) in self.colors):
                # Then the game is over, and the winner is whoever's goal zone is full
                # This rule prevents blocking: if you sit in an opponent's goal zone,
                #   then your piece counts towards their completion.
                self.winner = CheckersGame.opposite(FULL_BOARD[end])
        else:
            # Otherwise it's the next player's turn
            self.player_turn = (self.player_turn + 1) % self.n_players

    def is_legal(self, start, end):
        """Determines whether a move is legal.
           Does not check turn order.
        """
        return self._index_on_board(start)             \
                and self._index_on_board(end)          \
                and self._board[start] > 0             \
                and self._check_zone_locks(start, end) \
                and self.exists_path(start, end)
    
    def get_legal(self, player):
        """Generator yielding the all legal moves for
           a certain player.
        """
        for start in filter(
                lambda k: self._board[k] == self.colors[player],
                np.ndindex(self._board.shape)):
            yield from (
                    {"start": start, "end": end}
                    for end in self.paths(start)
                    if self._check_zone_locks(start, end)
                )

    
    def paths(self, start):
        """Generator that yields all the points that a given
           piece can move to by hopping or single-adjacency.
        """
        # Unrolling 2-tuple addition will make it fast
        tupadd = lambda p, v: (p[0] + v[0], p[1] + v[1])
        # First, we'll check adjacency moves.
        adj = [tupadd(start, v) for v in DIRECTIONS]
        yield from (p for p in adj if self.board(p) == 0)
        # Now we check repeated hops.
        # We do this by a breadth first search.
        visited = set(adj)
        to_visit = [start]
        while len(to_visit):
            pt = to_visit.pop(0)
            yield pt
            
            visited.add(pt)
            # Compute the hop directions
            dirs = ((tupadd(pt, v), tupadd(pt, tupadd(v, v))) for v in DIRECTIONS)
            to_visit.extend(
                    dest for over, dest in dirs
                        if self.board(over) > 0
                        and self.board(dest) == 0
                        and dest not in visited
                )
    
    def exists_path(self, start, end):
        """Checks if it is possible to move a piece from
           the start to the end.
        """
        for dest in self.paths(start):
            if dest == end:
                return True
        return False

    def _check_zone_locks(self, start, end):
        """There are various reasons that a piece may
           be forbidden from moving to a certain spot,
           regardless of whether there is a path.
           This method checks those conditions.

           returns:
               True if the move might be allowed,
               False if the move is forbidden.
        """
        color = self._board[start]
        goal = CheckersGame.opposite(color)

        start_zone = FULL_BOARD[start]
        end_zone = FULL_BOARD[end]

        # You can always get into your own goal
        #   and you can always move within a zone.
        if end_zone == start_zone or end_zone == goal:
            return True
        # So now we can assume they changed zones.
        # And that if they're in a goal, it's not their own.

        # The first rule is that if a piece is in *its destination goal*,
        #   it can't be moved outside of it.
        if start_zone == goal:
            return False
        # The second rule is that we may not move into a zone which is
        #   another player's spawn or goal
        # So if you end up in a goal zone (that isn't your goal),
        #   or you end up in a spawn zone that isn't your spawn
        #   then you've violated this rule.
        if (self.opposite(end_zone) in self.colors) or \
           (end_zone in self.colors and end_zone != color):
               return False

        return True

    def _index_on_board(self, point):
        s = self._board.shape
        return 0 <= point[0] < s[0] and 0 <= point[1] < s[1]

    def board(self, point):
        return self._board[point] if self._index_on_board(point) else -1

    def __str__(self):
        b = self._board.tolist()
        
        return '\n'.join(
                ''.join(" " if i == -1 else "o" if i == 0 else str(i) for i in row)
                for row in b)


# Fixed board layout
_BOARD_STR = """\
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
# I want to zero-index the colors, but instead I'm going to make 0 be the empty space
_BOARD_INT_MAP = {
    '.': -1, 'o': 0,
    '1': 1, '2': 2, '3': 3,
    '4': 4, '5': 5, '6': 6
}
FULL_BOARD = np.array(
    [[_BOARD_INT_MAP[c] for c in r] for r in _BOARD_STR.splitlines()],
    dtype=np.int8)

START_ZONES = [[] for _ in range(7)]
for ind in np.ndindex(FULL_BOARD.shape):
    START_ZONES[FULL_BOARD[ind]].append(ind)

DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
    (-1, -1),
    (1, 1)
]
