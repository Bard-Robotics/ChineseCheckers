import game
from ffi import legal_moves, ffi # type: ignore
import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Union

WIN_VALUE = 10000

Move = Tuple[Tuple[int, int], Tuple[int, int]]

class MiniMaxer():

    def __init__(self):
        self.transposition_table = dict()


    def find_move(self, board: game.CheckersGame, depth: int):
        board_copy = game.CheckersGame(board._board, board.player_turn)
        move = None
        val = 0
        
        for d in range(1, depth+1):
            (val, move) = self.minimax(board_copy, d)
        print(f"Player {board.player_turn} has advantage of {val}")
        return move


    def minimax(self, board: game.CheckersGame, depth: int):
        (val, move) = self._minimax(board, -WIN_VALUE * 2, WIN_VALUE * 2, depth)
        assert move is not None
        return (val, move)


    def _minimax(self, board: game.CheckersGame,
            alpha: int, beta: int, depth: int) -> Tuple[int, Union[Move, None]]:
        
        # Transposition Table lookup
        alpha_orig = alpha
        # Lookup in the table
        key = board.hash()
        tt = self.transposition_table.get(key)
        if tt is not None and tt.depth >= depth:
            if tt.flag == Transposition.EXACT:
                return (tt.value, tt.principal)
            if tt.flag == Transposition.LOWER:
                alpha = max(alpha, tt.value)
            elif tt.flag == Transposition.UPPER:
                beta = min(beta, tt.value)

            if alpha >= beta:
                return (tt.value, tt.principal)
        
        if board.winner is not None or depth == 0:
            score =  self.score(board)
            return (score if board.player_turn == 1 else -score, None)

        # legal_moves is a wrapper around a cffi function
        moves = legal_moves(board)
        
        # Put the principal move first
        if tt is not None and tt.principal is not None:
            principal_index = moves.index(tt.principal)
            moves = [tt.principal] + moves[:principal_index] + moves[principal_index+1:]
        
        # This routine can probably be optimized.
        # Negamax with alpha-beta pruning
        value = -WIN_VALUE * 2
        best_move = None

        for move in moves:
            board.move(move[0], move[1], verify = False)
            (move_val, _) = self._minimax(board, -beta, -alpha, depth - 1)
            move_val = -move_val
            board._unmove()

            if move_val > value:
                value = move_val
                best_move = move

            alpha = max(alpha, value) 

            if alpha >= beta:
                # Record cutoff?
                break

        
        # Transposition Table store
        flag = Transposition.EXACT
        if value <= alpha_orig:
            flag = Transposition.UPPER
        elif value <= beta:
            flag = Transposition.LOWER

        self.transposition_table[key] = Transposition(value, depth, flag, best_move)
        
        return (value, best_move)


    def score(self, board: game.CheckersGame) -> int:
        """
        Score a board using terminal value or heuristic.
        Don't minimax or check the transposition table.

            Parameters:
                board (CheckersGame): A board to be scored.

            Returns:
                value (int): The estimated value of the position for player 1.
        """
        if board.winner is not None:
            return WIN_VALUE if board.winner == 1 else -WIN_VALUE
        # Call the heuristic
        return self.heuristic(board)


    def heuristic(self, board: game.CheckersGame) -> int:
        """
        Evaluate the strength of a position from player one's perspective.

            Parameters:
                board (CheckersGame): A board to be evaluated.
                    Evaluation should only take into account board.board
                    and board.player_turn.

            Returns:
                value (int): The estimated value of the position for player 1.
                    This value should be between -WIN_VALUE and WIN_VALUE.

        Override this method in your subclass! You should try to achieve a tradeoff between evaluation accuracy and runtime.
        """
        # Naive heuristic: player 1 wants to minimize the coordinates of all pieces.
        (y, x) = np.nonzero(board._board)
        # Type checker isn't smart enough to figure out that the sum of an int array is an int
        return 160 - (np.sum(y) + np.sum(x)) # type: ignore


    def order(self, board: game.CheckersGame, moves: List[Move]) -> List[Move]:
        """
        Order the given moves, attempting to put the most promising moves first in the list.
        This is known to give big speedups to Alpha-Beta pruning.

            Parameters:
                board: (CheckersGame): The board from which the moves come.
                moves:         (list): The list of legal moves for the current player.

            Returns:
                ordered_moves  (list): The same list of legal moves, but with the best moves
                    at the front.

        Override this method in your subclass! You should try to chieve a tradeoff between ordering accuracy and runtime.
        """
        return moves


@dataclass
class Transposition:
    value: int
    depth: int
    flag:  int
    principal: Union[Move, None]

    EXACT = 0
    LOWER = 1
    UPPER = 1
