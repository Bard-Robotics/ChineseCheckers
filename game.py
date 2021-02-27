from typing import TYPE_CHECKING
import numpy as np

class CheckersGame():
    """
    The state of one entire game board.
    """
   
    opposite = [0, 2, 1]

    def __init__(self, board = None, to_move: int = 1):
        # The board is a numpy array so that we can copy it really fast
        if board is None:
            board = FULL_BOARD
            to_move = 1
        self._board = np.copy(board)
        self.winner = None
        self.player_turn = to_move

    def move(self, start, end, verify=True) -> None:
        """
        Make a move inplace.

            Parameters:
                start (tuple): The location of the piece to be picked up.
                end   (tuple): The place to put the new piece.
                verify (bool): Whether or not to check legality of the move. Default: True. 
                               Checking move legality is slow, so disabling verification
                               during simulation or tree search for performance is helpful.

        """
        # Given a move, (ie, a piece location and a destination)
        #  check if the specified piece belongs to the player whose turn it is
        #  check if the move is legal using pathfinding algorithm
        #  update the board to reflect the change
        #  check if this move causes the game to be over
        if verify:
            assert self.is_legal(start, end)
            assert self._board[start] == self.player_turn
            assert self.winner is None
       
        # Move pieces
        self._board[end] = self._board[start]
        self._board[start] = 0

        # Check the winner
        # Is the destination in a home zone?
        if (FULL_BOARD[end] > 0
            # Is the home zone full?
            and all(self._board[i] > 0 for i in START_ZONES[self.player_turn])):
                # Then the game is over, and the winner is whoever's goal zone is full
                # This rule prevents blocking: if you sit in an opponent's goal zone,
                #   then your piece counts towards their completion.
                self.winner = self.player_turn
        else:
            # Otherwise it's the next player's turn
            self.player_turn = CheckersGame.opposite[self.player_turn]

    def is_legal(self, start, end) -> bool:
        """Determines whether a move is legal.
           Does not check turn order.

                Parameters:
                    start (tuple): Starting piece location.
                    end   (tuple): Ending piece location.

                Returns:
                    bool
        """
        return self.board(end) == 0                    \
                and self.board(start) > 0              \
                and self._check_zone_locks(start, end) \
                and self.exists_path(start, end)
    
    def get_legal(self, player):
        """Generator yielding the all legal moves for
           a certain player.

                Parameters:
                    player (int): Index of the player who is moving.

                Returns:
                    A generator yielding dicts of the form {"start": (y0, x0), "end": (y1, x1)}.

        """
        for start in map(tuple, np.argwhere(self._board == player)):
            yield from (
                    {"start": start, "end": end}
                    for end in self.paths(start)
                    if self._check_zone_locks(start, end)
                )

    
    def paths(self, start):
        """Generator that yields all the points that a given
           piece can move to by hopping or single-adjacency.

                Parameters:
                    start (tuple): Board location. There does not have to actually be a piece there.

                Returns:
                    Generator yielding (y, x) tuples of spaces that can be moved to.
        """
        # This is probably a little slow
        tupadd = lambda p, v: (p[0] + v[0], p[1] + v[1])
        # First, we'll check adjacency moves.
        adj = [tupadd(start, v) for v in DIRECTIONS]
        yield from (p for p in adj if self.board(p) == 0)
        # Now we check repeated hops.
        # We do this by a breadth first search.

        #TODO: Consensus on legality of hopping back to start and "skipping"
        visited = set(adj)
        to_visit = [start]
        while len(to_visit):
            pt = to_visit.pop(0)
            if pt in visited:
                continue

            # We have to actually move a piece
            # But this stops us from considering "start" even if we can
            #   make some hops and get back to start
            if pt is not start:
                yield pt
            
            visited.add(pt)
            # Compute the hop directions
            dirs = ((tupadd(pt, v), tupadd(pt, tupadd(v, v))) for v in DIRECTIONS)
            to_visit.extend(
                    dest for over, dest in dirs
                        if self.board(over) > 0
                        and self.board(dest) == 0
                        and dest not in visited
                        and over != start
                )
    
    def exists_path(self, start, end):
        """Checks if it is possible to move a piece from
           the start to the end.
        """
        return end in self.paths(start)

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
        goal = CheckersGame.opposite[color]

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
        # The second rule is that we may not move into a zone which is
        #   another player's spawn or goal
        if start_zone == goal or end_zone == color:
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
                ''.join("o" if i == 0 else str(i) for i in row)
                for row in b)

    def __hash__(self):
        """
        The hash of a game consists of the board state plus whose turn it is.
        """
        return hash((self._board.tobytes(), self.player_turn))
        
    def __eq__(self, other):
        if isinstance(other, CheckersGame):
            return np.array_equal(self._board, other._board) and self.player_turn == other.player_turn
        return NotImplemented

# Fixed board layout
_BOARD_STR = """\
222200000
222000000
220000000
200000000
000000000
000000001
000000011
000000111
000001111"""
# I want to zero-index the colors, but instead I'm going to make 0 be the empty space
FULL_BOARD = np.array(
    [[ int(c) for c in r] for r in _BOARD_STR.splitlines()],
    dtype=np.int8)

START_ZONES = [[] for _ in range(3)]
for ind in np.ndindex(FULL_BOARD.shape):
    col = FULL_BOARD[ind]
    START_ZONES[col].append(ind)

DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
    (-1, 1),
    (1, -1)
]
