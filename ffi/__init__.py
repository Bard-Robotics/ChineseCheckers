from ._legal_moves import ffi, lib # type: ignore
from typing import List, Tuple

Move = Tuple[Tuple[int, int], Tuple[int, int]]

def legal_moves(board) -> List[Move]:
    _board = ffi.from_buffer('unsigned char[9][9]', board._board);

    _ret = lib.getLegalMoves(_board, board.player_turn)

    moves = []
    while _ret != ffi.NULL:
        move = _ret.data
        (start, end) = (move.start, move.end)
        moves.append(((start.y, start.x), (end.y, end.x)))

        _ret = _ret.next

    return moves
