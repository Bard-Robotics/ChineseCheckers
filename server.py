import flask
from game import CheckersGame
from string import ascii_uppercase
from random import choices

app = flask.Flask(__name__)
games = dict()

@app.route('/')
def home():
    """Serve a page where the user can pick to join an existing game,
    or start a new game (with some settings)."""
    return flask.render_template('home.html')

@app.route("/room/<string:game_id>", methods=["GET"])
def gameRoom(game_id):
    """Serve a page where the user can see a live representation of a game."""
    if game_id not in games:
        flask.abort(404)
    return game_id

@app.route("/api/game/create", methods=["POST"])
def apiGameCreate():
    payload = flask.request.form
    if "players" not in payload or "time" not in payload:
        flask.abort(400)
    n_players = int(payload["players"])
    time_limit = max(int(payload["time"]), 0)
    if n_players not in [2, 3, 4, 6]:
        flask.abort(400)

    # We've checked the request, let's go ahead and generate an ID for the room.
    new_id = generate_id(games.keys())
    games[new_id] = CheckersGame.new_game(n_players, time_limit=time_limit)
    # And now we redirect the user to the newly-created room.
    return flask.redirect(flask.url_for("gameRoom", game_id=new_id))


@app.route("/api/game/<string:game_id>", methods=["GET", "HEAD"])
def apiGameState(game_id):
    """Return the current state of a game, encoded as JSON."""
    if game_id not in games:
        flask.abort(404)
    return flask.jsonify({"data": 0})

@app.route("/api/game/<string:game_id>/move", methods=["POST"])
def apiGameMove(game_id):
    # The user can send a JSON-encoded move WHEN IT IS THEIR TURN
    # They have to supply the secret key they were given when they joined
    # If it isn't their turn OR the secret key is wrong, return an error code.
    if not flask.request.json:
        flask.abort(400)
    payload = flask.request.json

# This is a static method; it's not routed to any endpoint
def generate_id(existing):
    """Generate a random 5-letter ID that's not already in a list."""
    # There are 11 million strings of five letters
    assert len(existing) < 1e6
    random_str = lambda: ''.join(choices(ascii_uppercase, k=5))
    candidate = random_str()
    while candidate in existing:
        # Try again!
        # The large stack here shouldn't be an issue since there's at most a 10% chance of a collision
        candidate = random_str()
    return candidate


if __name__ == '__main__':
    app.run(debug=True)
