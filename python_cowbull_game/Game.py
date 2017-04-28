import uuid
import json
from time import time
from python_digits import DigitWord
from .GameObject import GameObject


class Game:
    _g = None

    def __init__(self):
        pass

    def new_game(self):
        dw = DigitWord()
        dw.random(GameObject.digits_used["normal"])

        self._g = GameObject()
        _game = {
            "key": str(uuid.uuid4()),
            "status": "playing",
            "ttl": int(time()) + 3600,
            "answer": dw.word,
            "mode": "normal",
            "guesses_remaining": GameObject.guesses_allowed["normal"],
            "guesses_made": 0
        }
        self._g.from_json(jsonstr=json.dumps(_game))
        return self._g.to_json()

    def load_game(self, jsonstr):
        self._g = GameObject()
        self._g.from_json(jsonstr=jsonstr)

    def save_game(self):
        self._validate_game_object(op="save_game")
        return self._g.to_json()

    def guess(self, *args):
        self._validate_game_object(op="guess")
        _return_results = {
            "cows": None,
            "bulls": None,
            "analysis": [],
            "status": ""
        }
        _start_again = "{0} The correct answer was {1}. Please start a new game."

        if self._g.status.lower() == "won":
            _return_results["status"] = _start_again.format(
                "You already won!",
                self._g.answer.word
            )
        elif self._g.status.lower() == "lost":
            _return_results["status"] = _start_again.format(
                "You lost (too many guesses)!",
                self._g.answer.word
            )
        elif self._g.guesses_remaining < 1:
            _return_results["status"] = _start_again.format(
                "Sorry, you lost!",
                self._g.answer.word
            )
        elif self._g.ttl < time():
            _return_results["status"] = _start_again.format(
                "Sorry, you ran out of time!",
                self._g.answer.word
            )
        else:
            self._g.guesses_remaining -= 1
            self._g.guesses_made += 1
            guess = DigitWord(*args)
            _return_results["analysis"] = []
            _return_results["cows"] = 0
            _return_results["bulls"] = 0

            for i in self._g.answer.compare(guess):
                if i.match is True:
                    _return_results["bulls"] += 1
                elif i.in_word is True:
                    _return_results["cows"] += 1

                _return_results["analysis"].append(i.get_object())

            if _return_results["bulls"] == len(self._g.answer.word):
                self._g.status = "won"
                self._g.guesses_remaining = 0
            elif self._g.guesses_remaining < 1:
                self._g.status = "lost"
            _return_results["status"] = self._g.status

        return _return_results

    def _validate_game_object(self, op="unknown"):
        if self._g is None:
            raise ValueError(
                "Game must be instantiated properly before using - call new_game() "
                "or load_game(jsonstr='{...}')"
            )
        if not isinstance(self._g, GameObject):
            raise TypeError(
                "Unexpected error during {0}! GameObject (_g) is not a GameObject!".format(op)
            )
