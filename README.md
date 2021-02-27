# Chinese Checkers
Chinese Checkers playground for AIs, with multiplayer online evaluation mode.

### Prequisite
- Git and Github
- Python 
- Flask, numpy, request library for useful purposes
- Basic understanding of http requests + client/server relationship (conceptual)

## HTTP Api Documentation:
The API uses JSON and a very simple token-based authentication system. 

Note that the number of players has been locked at 2 in the game logic, but I haven't gotten around to updating the server. Sorry.
=======
## Running the game 
Download the repository, enter from the command line and run command ```python server.py```. This will give you a web address running on your local server that looks like ```http://127.0.0.1:5000/```, paste it in a web browser to view the game board. 

To interact with the server, get the room number ```ROOM_ID``` and web address ```HOST```. Run a client program (recommend using python or js) using the HTTP API to send requests to the game board. Here's a small sample program using the requests library in Python to move on checker piece.

```python
import requests 
roomid = "RGSHR"  # {GAME_ID}
HOST = "http:" # {HOST}

auth = requests.post(f"{HOST}/api/game/{roomid}/join")
token = auth.json()["token"]

requests.post(
    f"{HOST}/api/game/{roomid}/move", 
    headers={"Authorizatoin":f"Bearer{token}"}, 
    json={   "move":{"start":[13,10],"end":[12,10]} }
) 
```

#### Creating a room
```http
POST /api/game/create

{
    "players": num,
    "time": seconds
}
```
Returns `400` if the number of players isn't specified (the turn time limit is optional).
On success, returns a redirect to the newly created room.

#### Joining a room
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

#### Getting the state of a game
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

#### Making a move
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

## Python Library

Another way to use this library is to run offline CPU tournaments.

There is a minimax agent class that you can inherit from and define your own heuristic, move ordering, etc. 
We use `cffi` to optimize the game class so that minimax can run at a decent speed. Specifically, determining
the legal moves requires the a tree search, so we have implemented this function in C.
=======

