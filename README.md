# Chinese Checkers
Chinese Checkers playground for AIs, with multiplayer online evaluation mode.

## Objectives: 
- Learn how use git 
- Write Game Server
  - Language (JS, Python)
- Figure out standards for our online server.

## HTTP Api Documentation:
The API uses JSON and a very simple token-based authentication system.

#### Creating a room:
```http
POST /api/game/create

{
    "players": num,
    "time": seconds
}
```
Returns `400` if the number of players isn't specified (the turn time limit is optional).
On success, returns a redirect to the newly created room.

#### Joining a room:
```http
POST /api/game/<ROOM_ID>/join
```

Returns `400` if the room is already full.
Success response:
```
{
    "player": index,
    "token": token
}
```
The *token* must be saved in order to authenticate your moves later.   
The *player* index is which player you are, in turn order. See the following table for the colors that are used depending on the number of players:
| # | Colors           |
|---|------------------|
| 2 | 1, 4             |
| 3 | 1, 3, 5          |
| 4 | 1, 3, 4, 6       |
| 6 | 1, 2, 3, 4, 5, 6 |

So if you are assigned the index `2` in a 4-player game, then your pieces are colored `4`.

#### Getting the state of a game:
```http
GET /api/game/<ROOM_ID>
```

Response:
```
{
    "board": [ [...], ..., [...] ],
    "n_players": n,
    "time_limit": s,
    "last_played": t,
    "state": "waiting" | "finished" | "playing"
}
```
Additionally, each `state` value has an extra field that accompanies it.  
In the `waiting` state, the `joined` field indicates the number of players already in the lobby.  
In the `finished` state, the `winner` field indicates the index (or color?) of the player who won.  
In the `playing` state, the `turn` field indicates the index of the player whose turn it is.

The `board` is a 2D array indicating the current location of all pieces, with elements coded as follows.
| Value | Piece                     |
|-------|---------------------------|
|  -1   | Not part of the board     |
|   0   | Empty square              |
|  1-6  | Player-movable game piece |

#### Making a move:
```http
POST /api/game/<ROOM_ID>/move
Authorization: Bearer <TOKEN>

{
    "move": {"start": [y1, x1], "end": [y2, x2]}
}
```
Where `<TOKEN>` is the token you were returned when you joined the room.

If the token is not provided correctly, returns `401`.  
If the token doesn't match the player whose turn it is, or if the game is over or hasn't started, returns `403`.  
If the specified move is illegal, returns `400`.  
On success, returns `200` and no body.
