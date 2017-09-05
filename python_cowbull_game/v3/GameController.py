from python_cowbull_game.v3.GameMode import GameMode
from python_cowbull_game.v3.GameObject import GameObject
from python_digits import DigitWord
import copy
import json


class GameController(object):
    GAME_PLAYING = "playing"
    GAME_WAITING = "waiting"
    GAME_WON = "won"
    GAME_LOST = "lost"

    def __init__(
            self,
            game_json = None,
            game_modes = None
    ):
        # load game_modes
        self.game_modes = None
        self.load_game_modes(input_modes=game_modes)

        # load any game passed
        self.game = None
        self.load(game_json=game_json)

    #
    # 'public' methods
    #
    def load(self, game_json=None):
        if game_json is None:    # New game_json
            _game_object = GameObject(mode=self.game_modes[0])
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

    def load_game_modes(self, input_modes=None):
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

