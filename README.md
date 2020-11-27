# Chinese Checkers
Chinese Checkers playground for AIs, with multiplayer online evaluation mode.

## Objectives: 
- Learn how use git 
- Write Game Server
  - Language (Js, Python)
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
On sucess, returns a redirect to the newly created room.

#### Joining a room:
```http
POST /api/game/<ROOM_ID>/join
```

Returns `400` if the room is already full.
Success response:
```json
{
    "player": index,
    "token": token
}
```
The *token* must be saved in order to authenticate your moves later. 
The *player* index is which player you are, in turn order. See the following table for the colors that are used depending on the number of players:
| # | colors           |
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
```json
{
    // I'm still deciding the details here, haha
}
```

#### Making a move:
```http
POST /api/game/<ROOM_ID>/move
Authorization: Bearer <TOKEN>

{
    "move": [] // I'm still deciding the move encoding
}
```
Where `<TOKEN>` is the token you were returned when you joined the room.

If the token is not provided correctly, returns `401`.
If the token doesn't match the player whose turn it is, or if the game is over or hasn't started, returns `403`.
If the specified move is illegal, returns `400`.
On success, returns `200` and no body.
