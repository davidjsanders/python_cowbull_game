from time import time
from python_digits import DigitWord
from .GameObject import GameObject
import uuid


class Game:
    _g = None

    def __init__(self):
        pass

    def new_game(self):
        dw = DigitWord()
        dw.random(GameObject.digits_used["normal"])

        self._g = GameObject()
        self._g.initialize(
            key=str(uuid.uuid4()),
            status="playing",
            ttl=int(time()) + 3600,
            answer=dw,
            mode="normal",
            guesses_remaining=GameObject.guesses_allowed["normal"],
            guesses_made=0
        )
        return self._g.key

    def load_game(self, game_key):
        _test_str = self._fetch_game(game_key=game_key)
        self._g = GameObject()
        self._g.load(jsonstr=_test_str)

    def save_game(self):
        if self._g is None:
            raise ValueError(
                "Game must be instantiated properly before saving - call new_game() "
                "or load_game(game_key='21-21-21')"
            )
        if not isinstance(self._g, GameObject):
            raise TypeError(
                "Unexpected error during save_game! GameObject (_g) is not a GameObject!"
            )

        return self._g.dump()

    def _fetch_game(self, game_key):
        return '{"guesses_made": 0, "status": "playing", ' \
               '"ttl": {}, "mode": "normal", "guesses_remaining": 10, '.format(int(time())+3600) + \
               '"key": "123", "answer": [1, 0, 4, 7]}'
