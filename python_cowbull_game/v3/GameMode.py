import logging


class GameMode(object):
    def __init__(
            self,
            mode=None,
            priority=None,
            digits=None,
            digit_type=None,
            guesses_allowed=None,
            instruction_text=None,
            help_text=None
    ):
        # Initialize variables
        self._mode = None
        self._priority = None
        self._digits = None
        self._digit_type = None
        self._guesses_allowed = None
        self._instruction_text = None
        self._help_text = None

        # NOTICE: Properties are used to set 'private' fields (e.g. _mode) to handle
        # data validation in one place. When adding a new parameter to __init__ ensure
        # that the property is created (following the existing code) and set the
        # property not the 'internal' variable.
        #
        self.mode = mode
        self.priority = priority
        self.digits = digits
        self.digit_type = digit_type
        self.guesses_allowed = guesses_allowed
        self.instruction_text = instruction_text
        self.help_text = help_text

    #
    # Overrides
    #
    def __str__(self):
        return str(self.dump())

    def __repr__(self):
        return "<GameObject: mode: {}>".format(self._mode)

    #
    # Properties
    #
    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = self._property_setter(
            keyword="mode", required=True, datatype=str, value=value
        )

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        self._priority = self._property_setter(
            keyword="priority", required=True, datatype=int, value=value
        )

    @property
    def digits(self):
        return self._digits

    @digits.setter
    def digits(self, value):
        self._digits = self._property_setter(
            keyword="digits", required=False, default=4, datatype=int, value=value
        )

    @property
    def digit_type(self):
        return self._digit_type

    @digit_type.setter
    def digit_type(self, value):
        self._digit_type = self._property_setter(
            keyword="digit_type", required=False, default=0, datatype=int, value=value
        )

    @property
    def guesses_allowed(self):
        return self._guesses_allowed

    @guesses_allowed.setter
    def guesses_allowed(self, value):
        self._guesses_allowed = self._property_setter(
            keyword="guesses_allowed", required=False, default=10, datatype=int, value=value
        )

    @property
    def instruction_text(self):
        return self._instruction_text

    @instruction_text.setter
    def instruction_text(self, value):
        self._instruction_text = self._property_setter(
            keyword="instruction_text", required=False, datatype=str, value=value
        )

    @property
    def help_text(self):
        return self._help_text

    @help_text.setter
    def help_text(self, value):
        self._help_text = self._property_setter(
            keyword="help_text", required=False, datatype=str, value=value
        )

    #
    # 'public' methods
    #
    def dump(self):
        return {
            "mode": self._mode,
            "priority": self._priority,
            "digits": self._digits,
            "digit_type": self._digit_type,
            "guesses_allowed": self._guesses_allowed,
            "instruction_text": self._instruction_text,
            "help_text": self._help_text
        }

    #
    # 'private' methods
    #
    @staticmethod
    def _property_setter(
            keyword=None,
            required=None,
            default=None,
            datatype=None,
            value=None,
    ):
        _value = value
        logging.debug("_property_setter: Keyword=={} Value=={}".format(keyword, _value))

        if required and not _value and not default:
            raise KeyError("GameMode: '{}' not provided to __init__ and no default provided (or allowed).".format(keyword))

        if not _value and default is not None:
            _value = default

        if _value and not isinstance(_value, datatype):
            raise TypeError("{} is of type {} where {} was expected.".format(keyword, type(_value), datatype))

        logging.debug("_property_setter: Keyword=={} Value=={}".format(keyword, _value))
        return _value
