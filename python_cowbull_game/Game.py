from python_digits import DigitWord
from .GameObject import GameObject


class Game:
    g = None

    def __init__(self, key=None):
        if key is None:
            self.new_game()

    def new_game(self):
        dw = DigitWord()
        dw.random(GameObject.digits_used["normal"])

        self.g = GameObject(
            key="123",
            status="playing",
            ttl=3600,
            answer=dw,
            mode="normal",
            guesses_remaining=GameObject.guesses_allowed["normal"],
            guesses_made=0
        )

    def load_game(self, game_key):
        pass

    def dump(self):
        return self.g.dump()
