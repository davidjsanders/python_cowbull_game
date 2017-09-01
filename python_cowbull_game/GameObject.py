import uuid
from python_digits import DigitWord
from python_cowbull_game.GameMode import GameMode


class GameObject(object):
    GAME_WON = "won"
    GAME_PLAYING = "playing"
    GAME_LOST = "lost"

    game_states = [GAME_WON, GAME_LOST, GAME_PLAYING]

    def __init__(self, game_mode=None, source_dict: dict=None):
        self._validate_game_mode(game_mode)

        if source_dict:
            self.from_dict(source_dict=source_dict, game_mode=game_mode)
        else:
            dw = DigitWord(wordtype=game_mode.digit_type)
            dw.random(game_mode.digits)
            self._key = str(uuid.uuid4())
            self._status = self.GAME_PLAYING
            self._ttl = 3600
            self._answer = dw
            self._mode = game_mode.mode
            self._guesses_remaining = game_mode.guesses_allowed
            self._guesses_made = 0

    #
    # Properties
    #
    @property
    def mode(self):
        return self._mode

    @property
    def key(self):
        return self._key

    @property
    def ttl(self):
        return self._ttl

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not value in self.game_states:
            raise ValueError("Game status must be set to one of: {}".format(self.game_states))
        self._status = value

    @property
    def guesses_remaining(self):
        return self._guesses_remaining

    @guesses_remaining.setter
    def guesses_remaining(self, value):
        ex_msg = "Guesses remaining must be an integer, greater than or equal to zero."

        if not isinstance(value, int):
            raise TypeError(ex_msg)
        if value < 0:
            raise ValueError(ex_msg)

        self._guesses_remaining = value

    @property
    def guesses_made(self):
        return self._guesses_made

    @guesses_made.setter
    def guesses_made(self, value):
        ex_msg = "Guesses made must be an integer, greater than or equal to zero."

        if not isinstance(value, int):
            raise TypeError(ex_msg)
        if value < 0:
            raise ValueError(ex_msg)

        self._guesses_made = value

    @property
    def answer(self):
        return self._answer

    @property
    def answer_str(self):
        return ', '.join(str(d) for d in self._answer.word)

    #
    # 'public' methods
    #
    def to_dict(self):
        return {
            "key": self._key,
            "status": self._status,
            "ttl": self._ttl,
            "answer": self._answer.word,
            "mode": self._mode,
            "guesses_remaining": self._guesses_remaining,
            "guesses_made": self._guesses_made
        }

    def from_dict(self, source_dict=None, game_mode=None):
        self._validate_game_mode(game_mode)
        if not source_dict:
            raise ValueError("A valid dictionary must be passed as the source_dict")
        if not isinstance(source_dict, dict):
            raise TypeError("A valid dictionary must be passed as the source_dict. {} given.".format(type(source_dict)))

        required_keys = ("key", "status", "ttl", "answer", "mode", "guesses_remaining", "guesses_made")
        if not all(key in source_dict for key in required_keys):
            raise ValueError("The dictionary passed is malformed: {}".format(source_dict))

        self._key = source_dict["key"]
        self._status = source_dict["status"]
        self._ttl = source_dict["ttl"]
        self._answer = DigitWord(*source_dict["answer"], wordtype=game_mode.digit_type)
        self._mode = source_dict["mode"]
        self._guesses_remaining = source_dict["guesses_remaining"]
        self._guesses_made = source_dict["guesses_made"]

    def _validate_game_mode(self, game_mode=None):
        if not isinstance(game_mode, GameMode):
            raise TypeError("A valid {} must be passed as the game_mode".format(type(GameMode)))
