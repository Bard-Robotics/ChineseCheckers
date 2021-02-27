from ._legal_moves import ffi, lib # type: ignore

def legal_moves(board, player):
    _board = ffi.from_buffer('unsigned char[9][9]', board);

    _ret = lib.getLegalMoves(_board, player)

    while _ret != ffi.NULL:
        move = _ret.data
        (start, end) = (move.start, move.end)
        yield {'start': (start.y, start.x), 'end': (end.y, end.x)}
        _ret = _ret.next
