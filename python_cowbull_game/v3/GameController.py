from python_cowbull_game.v3.GameMode import GameMode
from python_cowbull_game.v3.GameObject import GameObject
from python_digits import DigitWord
import copy
import json
import logging


class GameController(object):
    GAME_PLAYING = "playing"
    GAME_WAITING = "waiting"
    GAME_WON = "won"
    GAME_LOST = "lost"

    def __init__(self, game_json=None, game_modes=None, mode=None):
        # load game_modes
        self.game_modes = None
        self.load_modes(input_modes=game_modes)

        # load any game passed
        self.game = None
        self.load(game_json=game_json, mode=mode)

    #
    # 'public' methods
    #
    def guess(self, *args):
        if self.game is None:
            raise ValueError("The Game is unexpectedly undefined!")

        response_object = {
            "bulls": None,
            "cows": None,
            "analysis": None,
            "status": None
        }

        if self.game.status == self.GAME_WON:
            response_object["status"] = \
                self._start_again_message("You already won!")
        elif self.game.status == self.GAME_LOST:
            response_object["status"] = \
                self._start_again_message("You already lost!")
        elif self.game.guesses_remaining < 1:
            response_object["status"] = \
                self._start_again_message("You've made too many guesses")
        else:
            guess_made = DigitWord(*args, wordtype=self.game.mode.digit_type)
            comparison = self.game.answer.compare(guess_made)

            self.game.guesses_made += 1
            response_object["bulls"] = 0
            response_object["cows"] = 0
            response_object["analysis"] = []

            for comparison_object in comparison:
                if comparison_object.match:
                    response_object["bulls"] += 1
                elif comparison_object.in_word:
                    response_object["cows"] += 1
                response_object["analysis"].append(comparison_object.get_object())

            if response_object["bulls"] == self.game.mode.digits:
                self.game.status = self.GAME_WON
                self.game.guesses_made = self.game.mode.guesses_allowed
                response_object["status"] = self._start_again_message(
                    "Congratulations, you win!"
                )
            elif self.game.guesses_remaining < 1:
                self.game.status = self.GAME_LOST
                response_object["status"] = self._start_again_message(
                    "Sorry, you lost!"
                )

        return response_object

    def load(self, game_json=None, mode=None):
        if game_json is None:    # New game_json
            if mode is not None:
                if isinstance(mode, str):
                    _game_object = GameObject(mode=self._match_mode(mode=mode))
                elif isinstance(mode, GameMode):
                    _game_object = GameObject(mode=mode)
                else:
                    raise TypeError("Game mode must be a GameMode or string")
            else:
                _game_object = GameObject(mode=self.game_modes[0])
            _game_object.status = self.GAME_PLAYING
        else:
            if not isinstance(game_json, str):
                raise TypeError("Game must be passed as a serialized JSON string.")

            game_dict = json.loads(game_json)

            if not 'mode' in game_dict:
                raise ValueError("Mode is not provided in JSON; game_json cannot be loaded!")

            _mode = GameMode(**game_dict["mode"])
            _game_object = GameObject(mode=_mode, source_game=game_dict)

        self.game = copy.deepcopy(_game_object)

    def save(self):
        return json.dumps(self.game.dump())

    def load_modes(self, input_modes=None):
        # Set default game modes
        _modes = [
            GameMode(
                mode="normal", priority=2, digits=4, digit_type=DigitWord.DIGIT, guesses_allowed=10
            ),
            GameMode(
                mode="easy", priority=1, digits=3, digit_type=DigitWord.DIGIT, guesses_allowed=6
            ),
            GameMode(
                mode="hard", priority=3, digits=6, digit_type=DigitWord.DIGIT, guesses_allowed=6
            ),
            GameMode(
                mode="hex", priority=4, digits=4, digit_type=DigitWord.HEXDIGIT, guesses_allowed=10
            )
        ]

        if input_modes is not None:
            if not isinstance(input_modes, list):
                raise TypeError("Expected list of input_modes")

            for mode in input_modes:
                if not isinstance(mode, GameMode):
                    raise TypeError("Expected list to contain only GameMode objects")
                _modes.append(mode)

        self.game_modes = copy.deepcopy(_modes)

    #
    # 'private' methods
    #
    def _match_mode(self, mode):
        _mode = [game_mode for game_mode in self.game_modes if game_mode.mode == mode]
        if len(_mode) < 1:
            raise ValueError("Mode {} not found - has it been initiated?".format(mode))
        _mode = _mode[0]

        if not _mode:
            raise ValueError("For some reason, the mode is defined but unavailable!")

        return _mode

    def _start_again_message(self, message=None):
        """Simple method to form a start again message and give the answer in readable form."""
        logging.debug("Start again message delivered: {}".format(message))
        the_answer = ', '.join(
            [str(d) for d in self.game.answer][:-1]
        ) + ', and ' + [str(d) for d in self.game.answer][-1]

        return "{0}{1} The correct answer was {2}. Please start a new game.".format(
            message,
            "." if message[-1] not in [".", ",", ";", ":", "!"] else "",
            the_answer
        )
