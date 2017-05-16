# python_cowbull_game

| Warning                                                |
|--------------------------------------------------------|
|This documentation is still work in progress - 5/14/17  |

**Version 1.0**
This is part 2 of a multi-part tutorial. The link for the tutorial will be provided soon.
This is an open source project and you are welcome to reuse and/or fork it.

**Related Projects**
* [python_digits](https://github.com/dsandersAzure/python_digits) : The python_digits object
used as the base of this game.
* [python_cowbull_server](https://github.com/dsandersAzure/python_cowbull_server) : A Flask
based server which serves up a web server offering the game to callers (human or machine)
* [python_cowbull_console](https://github.com/dsandersAzure/python_cowbull_console) : A
console based game which interacts with the server
* [python_cowbull_webapp](https://github.com/dsandersAzure/python_cowbull_webapp) : A single
page webapp which interacts with the web server using XHR (XMLHttpRequest).

Game is a class based cowbull game where the objective is to guess a sequence of numbers.
The numbers are randomly generated and the user is given a number of turns to guess the
numbers. The numbers are python-digits (integers between 0 and 9).

The game is started by instantiating a game object, g = Game(), and then calling the new
game method, g.new_game(). If you run this in the console, you will notice that it returns
the complete game object (including the answer) - that's because the Game object is
intended to be connected (or interfaced) to a user interface.

A game object is a JSON structure as follows:

```
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
```

The objective behind this project is to provide a Python function which provides a game
object representing a set of digits to be guessed. If the digit is correct and in the
correct sequence, then it is a bull; if the digit is correct but in the wrong place, then
it is a cow.

## Installation
After forking this repository (or cloning using https), the package can be installed typing

```pip install .```

and will then be available to your Python environment. Virtualenv is recommended to avoid polluting your
Python environment. The Python package is also available at
https://pypi.python.org/pypi?name=python-cowbull-game&:action=display and can be installed using
pip:

```pip install python_cowbull_game```

## Tests
When installing the package from source, tests are held in a directory called (unsurprisingly) tests.
To validate the package, run the tests as follows from the installation directory:

```python -m unittest python_cowbull_game.tests```

Add new tests into new files in the tests directory and update __init__.py to import them, then
tests can be run using the command above. *Hint* Use -v python_cowbull_game.tests to see the test results
in verbose mode.

## Usage
To use the package, do the following steps:

```
$ python
>>> from python_cowbull_game import Game
>>> g = Game()
>>> g.new_game(mode) # Mode is one of 'easy', 'normal', or 'hard'
'{"status": "playing", "guesses_made": 0, "ttl": 1494903060, "mode": "normal",
"key": "**uuid**", "guesses_remaining": 10, "answer": [6, 1, 4, 7]}'
>>> g.guess(1, 2, 3, 4)
# A dict of the analysis
>>> g.guess(4, 3, 2, 1)
>>> g.save_game() # Returns a JSON string for the caller to save
>>> g.load_game(jsonstr:str) # Loads a game from the JSON string provided
>>> g.digits_required # Returns the number of digits expected for the mode
>>> g.guesses_allowed # Returns the number of guesses allowed
>>> g.key             # Returns the uuid key for the game
```
This package is not really designed to be used 'stand-alone'; it is normally
consumed by a non-human caller, such as a game server.

## Game class
A Game provides an object representing a cowbull game. The game object tracks the
DigitWord secret, the guesses, and success or failure. Persistence is handled by
passing the Game object back and forth as a JSON string, as an external caller
is expected to provide the persistence layer.

* Instantiation: ```obj = Game()```
  * ``new_game(mode:str)`` : Start a new game with a new key. The mode is one
  of easy, normal, or hard. This can be extended (e.g. crazy) by modifying game_modes,
  digits_used, and guesses_allowed in GameObject.
  * ``save_game`` : Return a JSON dump of the GameObject.
  * ``load_game(jsonstr:str)`` : Take a string of dumped JSON and load it into a game
  object
  * ``guess(*args)`` : Make a guess with a variable list of Digits
* Properties:
  * ``digits_required:int``. Returns the number of Digits expected for a guess (get only)
  * ``guesses_allowed:int``. Returns the number of guesses allowed for the game (depends
  upon the game mode) (get only)
  * ``key:str``. Returns the unique UUID game key.



## DigitWord class
A DigitWord is a collection of Digit objects (see Digit). The collection can be any size (up to the
maximum size of a list.) The DigitWord holds each Digit in a list (see word) and DigitWord(s)
may be checked for equality and compared to another DigitWord providing analysis of the
matches (true or false), inclusion in the list (true or false, i.e. the number is the DigitWord
but not in the same position), and if the Digit occurrs more than once (true or false)

* Instantiation: ```obj = DigitWord(*args)``` (a variable, or null, list of integers (or castable types) representing Digits.
* Methods
  * ``__str__`` : Provide a string representation of the DigitWord
  * ``__eq__`` : Provide equality checking
  * ``__iter__`` : Provide iteration of the DigitWord
  * ``__len__`` : Provide length (i.e. number of Digits) of the DigitWord
  * ``dump()`` : return a JSON string representing the list
  * ``load(value:str)`` : load a JSON string as the value of the DigitWord
  * ``random(length:int=4)`` : Randomize the contents of the DigitWord
  * ``compare(other:DigitWord)`` : Compare (analyse) the Digits of another DigitWord against self
* Properties
  * ``word:list``. Returns the Digits in the DigitWord as a list of int

## DigitWordAnalysis class
A DigitWordAnalysis represents the analysis of a digit compared to the digits within a DigitWord.
The analysis states the index of the digit (0, 1, 2, etc.), the value of the digit (an integer
between 0 and 9), whether it matched the exact position in the DigitWord (True or False),
whether it occurred multiple times (True or False), and whether the digit was in the DigitWord
or not (True or False).

* Instantiation: ``obj = DigitWordAnalysis(index:int, digit:Digit, match:bool, in_word:bool, multiple: bool)``
* Methods:
  * ``get_object()``: Return a dictionary representing the analysis:
    * {'index': self._index, 'digit': self._digit, 'match': self._match, 'multiple': self._multiple, 'in_word': self._in_word}
* Properties
  * ``index: int``
  * ``digit: int``
  * ``match: bool``
  * ``in_word: bool``
  * ``multiple: bool``
