from uuid import uuid4
from python_digits import DigitWord, DigitWordAnalysis
import json
import logging
import socket


class OldGame:
    _key = None
    _status = None
    _ttl = 3600
    _answer = None
    _mode = None
    _guesses_remaining = None
    _guesses_made = None
    _last_guess = None

    game_modes = ["easy","normal","hard","crazy"]

    digits_used = {
        'easy': 3,
        'normal': 4,
        'hard': 4,
        'crazy': 10
    }

    guesses_allowed = {
        'easy': 10,
        'normal': 6,
        'hard': 3,
        'crazy': 3
    }

    def __init__(self, *args, **kwargs):
        self._initialize(*args, **kwargs)

    def _initialize(self, **kwargs):
        #
        # Validate game mode
        #
        logging.debug('OldGame.py: Validating game mode (if present)')
        mode = kwargs.get('mode', 'normal')
        if mode is not None:
            if mode.lower() not in Game.game_modes:
                raise ValueError('Game mode must be one of: {0}'.format(Game.game_modes))
        self._mode = mode.lower()
        logging.debug('OldGame.py: Game mode set to {0}'.format(self._mode))

        #
        # Check if existing game
        #
        logging.debug('OldGame.py: Validating game object (if present)')
        game_object = kwargs.get('game_object', None)
        if game_object is None:
            logging.debug('OldGame.py: Game object NOT provided; creating new.')
            dw = DigitWord()
            dw.random(length=self.digits_used[self._mode])
            game_object = {
                'answer': dw.word,
                'status': 'playing',
                'key': str(uuid4()),
                'ttl': 3600,
                'mode': self._mode,
                'guesses_remaining': self.guesses_allowed[self._mode],
                'guesses_made': 0,
                'last_guess': {}
            }

        logging.debug('OldGame.py: Game object created')
        self.load_object(game_object)

    @property
    def key(self):
        return self._key

    @property
    def ttl(self):
        return self._ttl

    @property
    def length(self):
        return self.digits_used[self._mode]

    @property
    def game(self):
        return json.dumps(
            {
                "game_id": self._key,
                "number_of_digits": self.digits_used[self._mode],
                "guesses_remaining": self._guesses_remaining,
                "time_to_live": self._ttl,
                "container": socket.gethostname()
            }
        )

    def load_object(self, game_object=None):
        if game_object is None:
            raise ValueError('Game Object cannot be None. It must be a JSON string with a dict.')
        if isinstance(game_object, str):
            _object = json.loads(game_object)
        elif isinstance(game_object, dict):
            _object = game_object
        else:
            raise TypeError('Game object must be a JSON string or well formatted dict')

        if not isinstance(_object, dict):
            raise TypeError('Game object must deserialize to a dict')

        self._answer = DigitWord(*_object.get('answer'))
        self._status = _object.get('status')
        self._key = _object.get('key')
        self._ttl = _object.get('ttl')
        self._mode = _object.get('mode')
        self._guesses_remaining = _object.get('guesses_remaining')
        self._guesses_made = _object.get('guesses_made')
        self._last_guess = _object.get('last_guess')

    def dump_object(self):
        _object = {
            'answer': self._answer.word,
            'status': self._status,
            'key': self._key,
            'ttl': self._ttl,
            'mode': self._mode,
            'guesses_remaining': self._guesses_remaining,
            'guesses_made': self._guesses_made,
            'last_guess': self._last_guess
        }
        return json.dumps(_object)

    def guess(self, digit_list=None):
        last_guess = self._last_guess
        if last_guess == {}:
            last_guess = None

        if last_guess is not None and self._status == 'success':
            return self._already_guessed()
        elif self._guesses_remaining < 1:
            return self._too_many_guesses()
        else:
            return self._process_guess(guess_word=DigitWord(*digit_list))

    def old_guess(self, digit_list=None):
        return self._process_guess(guess_word=DigitWord(*digit_list))
        #if "key" not in kwargs:
        #    raise ValueError("No key provided")

    def _already_guessed(self):
        return {
            'status': 'error',
            'message': 'You already guessed correctly',
            'answer': self._answer.word
        }

    def _too_many_guesses(self):
        return {
            'status': 'error',
            'message': 'Too many attempts to guess',
            'guesses-allowed': self.guesses_allowed[self._mode],
            'answer': self._answer.word
        }

    def _process_guess(self, guess_word):
        self._status = 'incorrect'
        cows = 0
        bulls = 0
        multiples = 0
        analysis_results = []

        self._guesses_remaining -= 1
        self._guesses_made += 1

        analysis = self._answer.compare(guess_word)
        for a in analysis:
            bulls += 1 if a.match else 0
            cows += 1 if a.in_word else 0
            analysis_results.append(a.get_object())

        if bulls == self.digits_used[self._mode]:
            self._status = 'success'
        else:
            if self._guesses_remaining == 0:
                self._status = 'failed'

        return_object = {
            'status': 'in-play',
            'cows': cows,
            'bulls': bulls,
            'multiples': multiples,
            'analysis': analysis_results
        }

        self._last_guess = return_object

        return return_object
