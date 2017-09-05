from python_digits.DigitWord import DigitWord
from python_cowbull_game.v3.GameMode import GameMode
import uuid


class GameObject(object):
    def __init__(
            self,
            mode=None,
            source_game=None
    ):
        if mode is None:
            raise ValueError(
                "A GameMode must be provided to start or load a game object"
            )
        if not isinstance(mode, GameMode):
            raise TypeError(
                "The mode passed to the game is not a GameMode!"
            )

        self._key = None
        self._status = None
        self._ttl = None
        self._answer = None
        self._mode = None
        self._guesses_remaining = None
        self._guesses_made = None

        if source_game:
            self.load(source=source_game)
        else:
            self.new(mode=mode)

    #
    # Properties
    #
    @property
    def key(self):
        return self._key

    @property
    def mode(self):
        return self._mode

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not isinstance(value, str):
            raise TypeError("Status is expected to be a constant from GameController")
        self._status = value

    @property
    def ttl(self):
        return self._ttl

    @property
    def answer(self):
        return self._answer

    @property
    def guesses_made(self):
        return self._guesses_made

    @guesses_made.setter
    def guesses_made(self, value):
        if not isinstance(value, int):
            raise TypeError("Expected int")
        self._guesses_made = value

    @property
    def guesses_remaining(self):
        return self.mode.guesses_allowed - self._guesses_made

    #
    # 'public' methods
    #
    def dump(self):
        return {
            "key": self._key,
            "status": self._status,
            "ttl": self._ttl,
            "answer": self._answer.word,
            "mode": self._mode.dump(),
            "guesses_made": self._guesses_made
        }

    def load(self, source=None):
        if not source:
            raise ValueError("A valid dictionary must be passed as the source_dict")
        if not isinstance(source, dict):
            raise TypeError("A valid dictionary must be passed as the source_dict. {} given.".format(type(source)))

        required_keys = (
            "key",
            "status",
            "ttl",
            "answer",
            "mode",
            "guesses_made")
        if not all(key in source for key in required_keys):
            raise ValueError("The dictionary passed is malformed: {}".format(source))

        _mode = GameMode(**source["mode"])
        self._key = source["key"]
        self._status = source["status"]
        self._ttl = source["ttl"]
        self._answer = DigitWord(*source["answer"], wordtype=_mode.digit_type)
        self._mode = _mode
        self._guesses_made = source["guesses_made"]

    def new(self, mode=None):
        dw = DigitWord(wordtype=mode.digit_type)
        dw.random(mode.digits)

        self._key = str(uuid.uuid4())
        self._status = ""
        self._ttl = 3600
        self._answer = dw
        self._mode = mode
        self._guesses_remaining = mode.guesses_allowed
        self._guesses_made = 0

    #
    # 'private' methods
    #
