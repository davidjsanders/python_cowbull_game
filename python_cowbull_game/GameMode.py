import json
import logging
from python_digits import DigitWord


class GameMode(object):
    def __init__(self, **kwargs):
        self._data = {
            "mode": None,
            "digits": None,
            "digitType": None,
            "guesses_allowed": None,
            "instructions": None,
            "help": None
        }
        self._kw_handler(keyword="mode", required=True, datatype=str, **kwargs)
        self._kw_handler(keyword="digits", required=True, default=4, datatype=int, **kwargs)
        self._kw_handler(keyword="digitType", required=False, default=0, datatype=int, **kwargs)
        self._kw_handler(keyword="guesses_allowed", required=False, default=4, datatype=int, **kwargs)
        self._kw_handler(keyword="instructions", required=False, datatype=str, **kwargs)
        self._kw_handler(keyword="help", required=False, datatype=str, **kwargs)

    #
    # Overrides
    #
    def __str__(self):
        return "Mode: {}, ".format(self._data["mode"])+ \
               "digits: {}, ".format(self._data["digits"])+ \
               "type: {}, ".format(self._data["digitType"])+ \
               "guesses: {}, ".format(self._data["guesses_allowed"])+ \
               "instructions available: {}, ".format(self._data["instructions"] is not None)+ \
               "help available: {}".format(self._data["help"] is not None)

    def __repr__(self):
        return "<GameObject: mode: {}>".format(self._data["mode"])

    def __getattr__(self, name):
        return self._data[name]

    def __getitem__(self, item):
        return self._data[item]

    #
    # 'public' methods
    #

    #
    # 'private' methods
    #
    def _kw_handler(
            self,
            keyword,
            required=None,
            default=None,
            datatype=None,
            **kwargs
    ):
        _value = kwargs.get(keyword, None)
        logging.debug("_kw_handler: Keyword=={} Value=={}".format(keyword, _value))

        if required and not _value and not default:
            raise KeyError("GameMode: '{}' not provided to __init__ and no default provided.".format(keyword))

        if not _value and default is not None:
            _value = default

        if _value and not isinstance(_value, datatype):
            raise TypeError("{} is of type {} where {} was expected.".format(keyword, type(_value), datatype))

        self._data[keyword] = _value

        logging.debug("_kw_handler: Keyword=={} Value=={}".format(keyword, _value))
        return
