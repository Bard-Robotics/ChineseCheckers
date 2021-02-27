#pragma once
#include <stdint.h>
#include <stdbool.h>

// This stuff gets exported
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

// This stuff doesn't need to get exported
Point pointAdd(Point a, Point b);

// This function is so small that calling it from python would be a waste.
bool zoneLocks(Point start, Point end, unsigned char color);

// FILO queue
typedef struct pt_node {
    Point data;
    struct pt_node* next;

} PointNode;

PointNode* stackPush(PointNode* stack, Point data);
Point stackPop(PointNode** stack);

// Yielding
MoveNode* retPush(MoveNode* ret, Move data);
