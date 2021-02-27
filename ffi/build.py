from cffi import FFI
ffibuilder = FFI()

ffibuilder.cdef("""
    typedef struct pt {
        int y;
        int x;
    } Point;

    typedef struct move2 {
        Point start;
        Point end;
    } Move;

     typedef struct move2_node {
        Move data;
        struct move2_node* next;
     } MoveNode;

     MoveNode* getLegalMoves(unsigned char board[9][9], unsigned char player);
    """);

ffibuilder.set_source("_legal_moves",
        """
        #include "legal.h"
        """,
#        extra_compile_args = ["-O3",
#           "-ftree-vectorize",
#           "-msse2",
#           "-mfpmath=sse"],
        sources = ["legal.c"])

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
