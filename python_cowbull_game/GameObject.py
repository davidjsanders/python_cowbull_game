import json
from python_digits import DigitWord
from jsonschema import validate


class GameObject:
    _key = None
    _status = None
    _ttl = 3600
    _answer = None
    _mode = None
    _guesses_remaining = None
    _guesses_made = None
    _last_guess = None

    game_modes = ["easy", "normal", "hard"]
    game_states = ["won", "lost", "playing"]

    schema = {
        "type": "object",
        "properties":
            {
                "key": {"type": "string"},
                "status": {"type": "string"},
                "ttl": {"type": "integer"},
                "answer": {
                    "type": "array",
                    "items":
                        {
                            "digit":
                                {
                                    "type": "integer",
                                    "minimum": 0
                                }
                        }
                },
                "mode": {"type": "string"},
                "guesses_remaining": {"type": "integer"},
                "guesses_made": {"type": "integer"}
            }
    }

    digits_used = {
        'easy': 3,
        'normal': 4,
        'hard': 6
    }

    guesses_allowed = {
        'easy': 15,
        'normal': 10,
        'hard': 6
    }

    def __init__(
        self,
        key,
        status,
        ttl,
        answer,
        mode,
        guesses_remaining,
        guesses_made
    ):
        self.key = key
        self.status = status
        self.ttl = ttl
        self.answer = answer
        self.mode = mode
        self.guesses_remaining = guesses_remaining
        self.guesses_made = guesses_made

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value.lower() not in self.game_states:
            raise ValueError("Status can only be one of: {}".format(self.game_states))
        self._status = value

    @property
    def ttl(self):
        return self._ttl

    @ttl.setter
    def ttl(self, value):
        if not isinstance(value, int):
            raise TypeError("TTL must be an integer representing seconds")
        self._ttl = value

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, value):
        if not isinstance(value, DigitWord):
            raise TypeError("Answer must be a DigitWord")
        self._answer = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value not in self.game_modes:
            raise ValueError("Mode must be one of : {}".format(self.game_modes))
        self._mode = value

    @property
    def guesses_remaining(self):
        return self._guesses_remaining

    @guesses_remaining.setter
    def guesses_remaining(self, value):
        self._guesses_remaining = value

    @property
    def guesses_made(self):
        return self._guesses_made

    @guesses_made.setter
    def guesses_made(self, value):
        self._guesses_made = value

    def dump(self):
        return json.dumps(
            {
                "key": self._key or None,
                "status": self._status or None,
                "ttl": self._ttl or None,
                "answer": self._answer.word or None,
                "mode": self._mode or None,
                "guesses_remaining": self._guesses_remaining or None,
                "guesses_made": self._guesses_made or None
            }
        )

    def load(self, jsonstr):
        if not isinstance(jsonstr, str):
            raise TypeError("Load requires a valid JSON string")
        _temp_dict = json.loads(jsonstr)

        # Validate the dictionary object against the schema
        validate(_temp_dict, self.schema)

        self.key = _temp_dict["key"]
        self.status = _temp_dict["status"]
        self.ttl = _temp_dict["ttl"]
        # Create a DigitWord based on the array of integers passed in the JSON
        self.answer = DigitWord(*_temp_dict["answer"])
        self.mode = _temp_dict["mode"]
        self.guesses_remaining = _temp_dict["guesses_remaining"]
        self.guesses_made = _temp_dict["guesses_made"]
