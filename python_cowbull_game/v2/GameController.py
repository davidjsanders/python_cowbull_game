import json
import logging

from python_cowbull_game.GameObject import GameObject
from python_digits import DigitWord

from python_cowbull_game.v2.GameMode import GameMode


class GameController(object):
    schema = {
        "type": "object",
        "properties":
            {
                "key": {"type": "string"},
                "status": {"type": "string"},
                "ttl": {"type": "integer"},
                "answer": {
                    "type": "array",
                    "items": { "digit": {"type": "string"}}
                },
                "mode": {"type": "string"},
                "guesses_remaining": {"type": "integer"},
                "guesses_made": {"type": "integer"}
            }
    }

    def __init__(self, game):
        """Initialize the Game."""
        super(GameController, self).__init__()
        self._game_modes = [
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

        if game:
            self.load(game=game)
        else:
            self._game = None
            self._mode = None

    #
    # Properties
    #

    @property
    def digits_required(self):
        self._validate()
        _mode = self._load_mode(self._mode)
        return _mode.digits

    @property
    def digits_type(self):
        self._validate()
        _mode = self._load_mode(self._mode)
        return _mode.digit_type

    @property
    def guesses_allowed(self):
        self._validate()
        _mode = self._load_mode(self._mode)
        return _mode.guesses_allowed

    @property
    def key(self):
        self._validate()
        return self._game.key

    @property
    def game_modes(self):
        return sorted(self._game_modes, key=lambda x: x.priority)

    @property
    def game_mode_names(self):
        return [game_mode.mode for game_mode in sorted(self._game_modes, key=lambda x: x.priority)]

    @property
    def game(self):
        return self._game

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value not in self.game_mode_names:
            raise ValueError("Unsupported game mode {}. Valid choices are {}".format(
                value, ', '.join(self.game_mode_names))
            )
        self._mode = value

    #
    # 'public' methods
    #
    def add_mode(self, game_mode=None):
        if game_mode is None:
            raise ValueError("game_mode must be provided!")

        if isinstance(game_mode, GameMode):
            print("Adding {}".format(game_mode.mode))
            self._game_modes.append(game_mode)
        elif isinstance(game_mode, list):
            for i in game_mode:
                self.add_mode(game_mode=i)
        else:
            raise TypeError("game_mode must be of type {}".format(GameMode))

    def remove_mode(self, index=None):
        if len(self._game_modes) < 1:
            raise IndexError("There are no game modes to remove!")
        if index is None or not isinstance(index, int) or index > len(self._game_modes):
            raise ValueError("Index (int) must be specified within valid range")
        del(self._game_modes[index])

    def replace_mode(self, index=None, game_mode=None):
        if game_mode is None:
            raise ValueError("game_mode must be provided!")

    def replace_modes(self, game_modes=None):
        ex_msg = "game_modes must be a list of {}".format(GameMode)

        if game_modes is None:
            raise ValueError(ex_msg)
        if not isinstance(game_modes, list):
            raise TypeError(ex_msg)

        self._game_modes = []
        for i in game_modes:
            self.add_mode(game_mode=i)

    def new(self, mode=None):
        if mode is None:
            _mode = self._game_modes[0]
        else:
            self.mode = mode
            _mode = self._load_mode(mode)

        self._game = GameObject(game_mode=_mode)
        #return self._game

    def save(self):
        self._validate()
        return json.dumps(self._game.dump())

    def load(self, game=None):
        ex_msg = "Game must be passed as a serialized JSON string."

        if not game:
            raise ValueError(ex_msg)

        if not isinstance(game, str):
            raise TypeError(ex_msg)

        game_dict = json.loads(game)

        if not 'mode' in game_dict:
            raise ValueError("Mode is not provided in JSON; game cannot be loaded!")
        _mode = self._load_mode(game_dict['mode'])

        self._game = GameObject(game_mode=_mode, source_dict=game_dict)

    def guess(self, *args):
        self._validate()
        """
        guess() allows a guess to be made. Before the guess is made, the method
        checks to see if the game has been won, lost, or there are no tries
        remaining. It then creates a return object stating the number of bulls
        (direct matches), cows (indirect matches), an analysis of the guess (a
        list of analysis objects), and a status.

        :param args: any number of integers (or string representations of integers)
        to the number of Digits in the answer; i.e. in normal mode, there would be
        a DigitWord to guess of 4 digits, so guess would expect guess(1, 2, 3, 4)
        and a shorter (guess(1, 2)) or longer (guess(1, 2, 3, 4, 5)) sequence will
        raise an exception.

        :return: a JSON object containing the analysis of the guess:

        {
            "cows": {"type": "integer"},
            "bulls": {"type": "integer"},
            "analysis": {"type": "array of DigitWordAnalysis"},
            "status": {"type": "string"}
        }

        """
        logging.debug("guess called.")
        logging.debug("Validating game object")
        self._validate(op="guess")

        logging.debug("Building return object")
        _return_results = {
            "cows": None,
            "bulls": None,
            "analysis": [],
            "status": ""
        }

        logging.debug("Check if game already won, lost, or too many tries.")
        if self._game.status == GameObject.GAME_WON:
            _return_results["message"] = self._start_again("You already won!")
        elif self._game.status == GameObject.GAME_LOST:
            _return_results["message"] = self._start_again("You have made too many guesses, you lost!")
        elif self._game.guesses_remaining < 1:
            _return_results["message"] = self._start_again("You have run out of tries, sorry!")
        else:
            logging.debug("Creating a DigitWord for the guess.")

            _mode = self._load_mode(self._game.mode)
            guess = DigitWord(*args, wordtype=_mode.digit_type)

            logging.debug("Validating guess.")
            self._game.guesses_remaining -= 1
            self._game.guesses_made += 1

            logging.debug("Initializing return object.")
            _return_results["analysis"] = []
            _return_results["cows"] = 0
            _return_results["bulls"] = 0

            logging.debug("Asking the underlying GameObject to compare itself to the guess.")
            for i in self._game.answer.compare(guess):
                logging.debug("Iteration of guesses. Processing guess {}".format(i.index))

                if i.match is True:
                    logging.debug("Bull found. +1")
                    _return_results["bulls"] += 1
                elif i.in_word is True:
                    logging.debug("Cow found. +1")
                    _return_results["cows"] += 1

                logging.debug("Add analysis to return object")
                _return_results["analysis"].append(i.get_object())

            logging.debug("Checking if game won or lost.")
            if _return_results["bulls"] == len(self._game.answer.word):
                logging.debug("Game was won.")
                self._game.status = GameObject.GAME_WON
                self._game.guesses_remaining = 0
                _return_results["message"] = "Well done! You won the game with your " \
                                             "answers {}".format(self._game.answer_str)
            elif self._game.guesses_remaining < 1:
                logging.debug("Game was lost.")
                self._game.status = GameObject.GAME_LOST
                _return_results["message"] = "Sorry, you lost! The correct answer was " \
                                             "{}".format(self._game.answer_str)
            _return_results["status"] = self._game.status

        logging.debug("Returning results.")
        return _return_results

    #
    # 'private' methods
    #
    def _start_again(self, message=None):
        """Simple method to form a start again message and give the answer in readable form."""
        logging.debug("Start again message delivered: {}".format(message))
        the_answer = self._game.answer_str

        return "{0} The correct answer was {1}. Please start a new game.".format(
            message,
            the_answer
        )

    def _load_mode(self, mode):
        _mode = [game_mode for game_mode in self._game_modes if game_mode.mode == mode]
        if len(_mode) < 1:
            raise ValueError("No mode was found for {}".format(mode))
        _mode = _mode[0]

        if not _mode:
            raise ValueError("For some reason, the mode is defined but unavailable!")
        return _mode

    def _validate(self, op="unknown"):
        """
        A helper method to provide validation of the game object (_g). If the
        game object does not exist or if (for any reason) the object is not a GameObject,
        then an exception will be raised.

        :param op: A string describing the operation (e.g. guess, save, etc.) taking place
        :return: Nothing
        """
        if self._game is None:
            raise ValueError(
                "GameController:{}: ".format(op) +
                "Game must be instantiated before using - call new() to start a new game, "
                "or load() to load from JSON."
            )

