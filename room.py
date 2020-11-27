from random import choices
from string import ascii_letters, digits
import time
from game import CheckersGame

class Room:
    AUTH_CORPUS = ascii_letters + digits
    def __init__(self, game, players=None, time_limit=0):
        self.game = game
        if players is None:
            self.players = []
        else:
            self.players = players
        self.time_limit = time_limit
        self.last_move = None

    def join(self):
        assert not self.full()
        # The bearer token is a 32 character string, where the last character is the player index
        # This just makes sure we'll never have two players in one room with the same token
        auth = ''.join(choices(Room.AUTH_CORPUS, k=31)) + str(len(self.players))
        self.players.append(auth)
        return (len(self.players) - 1, auth)

    def full(self):
        return len(self.players) == self.game.n_players

    def checkTimer(self):
        """Check the turn timer and reset it if it hasn't gone off."""
        if self.time_limit == 0:
            return True
        new_time = time.time()
        if self.last_move is not None and new_time - self.last_move > self.time_limit:
            # In this case, we should handle the forfeit here
            return False
        self.last_move = new_time
        return True

    def auth(self, key):
        """Check if the player is allowed to move.
        This does not determine if the move is legal,
        just that the player is who they say they are and that it's their turn."""
        # Make sure the token corresponds to a user
        try:
            player = self.players.index(key)
        except ValueError:
            return False
        # Make sure the token corresponds to the *right* user
        return player == self.game.player_turn and self.full()
        
