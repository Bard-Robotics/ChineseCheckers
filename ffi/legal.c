#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "legal.h"

#define IN_BOUNDS(PT)   (0 <= PT.x && PT.x < 9 && 0 <= PT.y && PT.y < 9)
#define ZONE(DIAG)      (DIAG <= 3) ? 2 : (DIAG >= 13)
#define uchar_t         unsigned char

Point pointAdd(Point a, Point b) {
    return (Point) {a.y + b.y, a.x + b.x};
}
const Point DIRECTIONS[6] = {
    {-1, 0},
    {1, 0},
    {0, -1},
    {0, 1},
    {-1, 1},
    {1, -1}
};

// Yieldy
MoveNode* retPush(MoveNode* ret, Move data) {
    MoveNode* head = (MoveNode*) malloc(sizeof(MoveNode));
    head->data = data;
    head->next = ret;

    return head;
}
// Stacky
PointNode* stackPush(PointNode* stack, Point data) {
    PointNode* head = (PointNode*) malloc(sizeof(PointNode));
    head->data = data;
    head->next = stack;
    return head;
}
Point stackPop(PointNode** stack) {
    // Grab the top element of the stack
    PointNode* head = *stack;

    // Grab its return value and find the next one
    Point ret = head->data;
    PointNode* next = head->next;

    // Update the stack pointer
    *stack = next;
    // Free the popped thing
    free(head);

    return ret;

}

MoveNode* getLegalMoves(uchar_t board[9][9], uchar_t player) {
    // We can reuse this
    char visited[9][9] = {{0}};
    MoveNode* ret_list = NULL;

    // We have to loop over the board to find pieces (unless we store where they are...) but we can stop early once we find all the player's pieces.
    int rem_points = 10;
    for (int y = 0; y < 9 && rem_points > 0; y++) {
        for (int x = 0; x < 9 && rem_points > 0; x++) {
            if (board[y][x] != player) continue;
            // We found one of the player's pieces. 
            // Mark it as Not There so we can't hop over it.
            board[y][x] = 0;
            // And found so that we don't try to move back to it
            visited[y][x] = 1;

            const Point start = {y, x};
            // Now we compute all the paths from this point.
            // First, single hops
            for (int i = 0; i < 6; i++) {
                Point adj = pointAdd(start, DIRECTIONS[i]);
                // Can't mark visited out of bounds
                if (!IN_BOUNDS(adj)) continue;
                // Mark visited
                visited[adj.y][adj.x] = 1;
                
                // Check destination empty and check zone locks
                if (!board[adj.y][adj.x] && zoneLocks(start, adj, player))
                    ret_list = retPush(ret_list, (Move) {start, adj});
            }
            // Now we'll pathfind
            PointNode* to_visit = stackPush(NULL, start);
            while (to_visit != NULL) {
                Point cur = stackPop(&to_visit);
                
                // The only time this will happen is if cur == start
                if (!visited[cur.y][cur.x]++ && zoneLocks(start, cur, player))
                    ret_list = retPush(ret_list, (Move) {start, cur});

                // Consider splitting this into two loops so that we can vectorize the addition?
                for (int i = 0; i < 6; i++) {
                    Point direction = DIRECTIONS[i];
                    Point o = pointAdd(cur, direction);
                    Point d = pointAdd(o, direction);

                    if (IN_BOUNDS(o) && board[o.y][o.x] &&
                        IN_BOUNDS(d) && !board[d.y][d.x] &&
                        !visited[d.y][d.x]) {

                        to_visit = stackPush(to_visit, d);
                    }
                         
                }

            }
            // Return the piece to its position
            board[y][x] = player;
            // Mark the number of pieces
            if (rem_points--)
                // If there's any more pieces left to find, reset visited
                memset(visited, 0, sizeof(char)*81);
        }
    }
    return ret_list;
}

bool zoneLocks(Point start, Point end, uchar_t color) {
    const uchar_t start_zone = ZONE(start.y + start.x);
    const uchar_t end_zone   = ZONE(  end.y +   end.x);
    const uchar_t goal       = color % 2 + 1;
    
    return (end_zone == start_zone) ||
           (end_zone == goal)       || !(
             (start_zone == goal)   ||
             (end_zone   == color));
}
