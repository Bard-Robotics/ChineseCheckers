from game import CheckersGame
from string import ascii_uppercase
from random import choices

import flask
from flask import Flask, render_template, abort, url_for, request, redirect

app = Flask(__name__)
games = dict()

@app.route('/')
def home():
    """Serve a page where the user can pick to join an existing game,
    or start a new game (with some settings)."""
    return render_template('home.html')

@app.route("/room/<string:game_id>", methods=["GET"])
def gameRoom(game_id):
    """Serve a page where the user can see a live representation of a game."""
    if game_id not in games:
        abort(404)
    room = games[game_id]
    # When we render, we need to embed the game's info in the page's javascript
    return render_template('livegame.html')

@app.route("/api/game/create", methods=["POST"])
def apiGameCreate():
    # This page can be send data either as json or as a form
    payload = request.json if request.json else request.form
    if "players" not in payload:
        abort(400)
    n_players = int(payload["players"])
    time_limit = max(payload.get("time", 0, type=int), 0)
    if n_players not in [2, 3, 4, 6]:
        abort(400)

    # We've checked the request, let's go ahead and generate an ID for the room.
    new_id = generateId(games.keys())
    games[new_id] = Room(CheckersGame.new_game(n_players), time_limit=time_limit)
    # And now we redirect the user to the newly-created room.
    return redirect(url_for("gameRoom", game_id=new_id))


@app.route("/api/game/<string:game_id>", methods=["GET", "HEAD"])
def apiGameState(game_id):
    """Return the current state of a game, encoded as JSON."""
    if game_id not in games:
        abort(404)
    return dict()

@app.route("/api/game/<string:game_id>/join", methods=["POST"])
def apiGameJoin(game_id):
    if game_id not in games:
        abort(404)
    room = games[game_id]
    if room.full():
        abort(400)
    (player_index, auth) = room.join()
    return dict(player=player_index, token=auth)

@app.route("/api/game/<string:game_id>/move", methods=["POST"])
def apiGameMove(game_id):
    # The user can send a JSON-encoded move WHEN IT IS THEIR TURN
    # And when the room is full
    # They have to supply the secret key they were given when they joined
    # If it isn't their turn OR the secret key is wrong, return an error code.
    if game_id not in games:
        abort(404)
    room = games[game_id]

    try:
        # This will throw an error if it doesn't exist
        auth = request.headers["Authorization"]
        # = "Bearer <token_here_.........>
        assert auth.startswith("Bearer")
        # The auth has a space after Bearer
        token = auth.split()[1]
    except:
        abort (401)
    # Ok, the user has provided authentication that we understand.
    if not room.auth(token):
        abort(403)
    # OK. The user's authentication is valid.
    # We know that it's their turn.
    # Now we can ask the game class if this move is legal.
    if not request.json or "move" not in request.json:
        abort(400)
    move = payload["move"]
    if not game.is_legal(move):
        abort(400)
    # Now we can make the move!
    room.checkTimer()
    game.move(move)
    
    return {}, 200

# This is a static method; it's not routed to any endpoint
def generateId(existing):
    """Generate a random 5-letter ID that's not already in a list."""
    # There are 11 million strings of five letters
    assert len(existing) < 1e6
    random_str = lambda: ''.join(choices(ascii_uppercase, k=5))
    candidate = random_str()
    while candidate in existing:
        # Try again!
        candidate = random_str()
    return candidate

if __name__ == '__main__':
    app.run(debug=True)
