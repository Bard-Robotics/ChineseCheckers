import flask
import game

app = flask.Flask(__name__)

@app.route('/')
def home():
    # When a user goes here, we want to serve them an HTML/JS page
    # On which they'll be able to see the game board.
    # I think we only need to have one game running on each server.
    # I guess if the game is full or has already started they can watch.
    # Otherwise assign them a secret key (basically, a session cookie which lets them send moves), and a color
    # We also need a way to start the game
    return "Some HTML"

@app.route("/api/state", methods=["GET"])
def get_state():
    # This should return the current state of the game. 
    # It should make it clear whose turn it is.
    return flask.jsonify({"data": 0})

@app.route("/api/move", methods=["POST"])
def make_move():
    # The user can send a JSON-encoded move WHEN IT IS THEIR TURN
    # They have to supply the secret key they were given when they joined
    # If it isn't their turn OR the secret key is wrong, return an error code.
    if not flask.request.json:
        abort(400)
    payload = flask.request.json

if __name__ == '__main__':
    app.run(debug=True)
