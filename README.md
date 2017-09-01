# python_cowbull_game

**Version 1.1.6**

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

**NOTE** This package is not designed to be consumed by a human at the Python level;
it is designed to be called by an API style program which will control the interaction
with the game and another (interface level) app, that will control user interaction. 
The reason for this is to enforce minimal coupling (a caller does not need to know
how the game operates) with maximum cohesion (each component does only what it is 
supposed to do.)

## Installation
After forking this repository (or cloning using https), the package can be installed typing

```pip install .```

and will then be available to your Python environment. Virtualenv is recommended to avoid polluting your
Python environment. The Python package is also available at [PyPi](https://pypi.python.org/pypi?name=python-cowbull-game&:action=display)
and can be installed using
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
>>> g.guesses_allowed # Returns the number of guesses_allowed allowed
>>> g.key             # Returns the uuid key for the game
```
This package is not really designed to be used 'stand-alone'; it is normally
consumed by a non-human caller, such as a game server.

The version 1.1.2 release adds inheritance, allowing the game object
to be superclassed and support more modes, for example:

```
$ python
>>> from python_cowbull_game import Game
>>> from python_cowbull_game import GameObject as BaseGO
>>> class GameObject(BaseGO):
...     game_modes = ["easy", "normal", "hard", "crazy", "mega"]
...     digits_used = {
...         'easy': 3,
...         'normal': 4,
...         'hard': 6,
...         'crazy': 10,
...         'mega': 5
...     }
...     guesses_allowed = {
...         'easy': 15,
...         'normal': 10,
...         'hard': 6,
...         'crazy': 10,
...         'mega': 3
...     }
...     def __init__(self):
...         super(GameObject, self).__init__()
...
>>> g = Game(game_object=GameObject)
>>>
```

## Game class
A Game provides an object representing a cowbull game. The game object tracks the
DigitWord secret, the guesses_allowed, and success or failure. Persistence is handled by
passing the Game object back and forth as a JSON string, as an external caller
is expected to provide the persistence layer.

* Instantiation: ```obj = Game()``` or ```obj = Game(game_object=GameObject)```
* Methods:
  * ``new_game(mode:str)`` : Start a new game with a new key. The mode is one
  of easy, normal, or hard. This can be extended (e.g. crazy) by modifying game_modes,
  digits_used, and guesses_allowed in GameObject.
  * ``save_game`` : Return a JSON dump of the GameObject.
  * ``load_game(jsonstr:str)`` : Take a string of dumped JSON and load it into a game
  object
  * ``guess(*args)`` : Make a guess with a variable list of Digits
* Properties:
  * ``digits_required:int``. Returns the number of Digits expected for a guess (get only)
  * ``guesses_allowed:int``. Returns the number of guesses_allowed allowed for the game (depends
  upon the game mode) (get only)
  * ``key:str``. Returns the unique UUID game key.



## GameObject class
A GameObject is a representation of a game object used to provide the attributes and
methods related to a game. It takes input and output as JSON and expects a match to a
specific schema:

```
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
```

* Instantiation: ```obj = GameObject()``` 
* Methods
  * ``to_json()`` : Dump the game object to JSON
  * ``from_json(jsonstr:str)`` : Load the game object from a JSON string
* Properties
  * ``game_modes:str`` : A list of allowed modes (easy, normal, hard, etc.).
  * ``game_states:str`` : A list of game states (playing, won, lost).
  * ``digits_used:int`` : The number of Digits used in the game (based on mode).
  * ``guesses_allowed:int`` : The number of guesses_allowed allowed for the game mode.
  * ``key:str`` : A string representation of a UUID 4 word unique identifier.
  * ``status:str`` : One of game_states above.
  * ``ttl:int`` : An integer representing the time at which the game key 
  should expire.
  * ``answer:DigitWord`` : The solution to the current game
  * ``mode:str`` : One of game_modes above.
  * ``guesses_remaining:int`` : The number of guesses_allowed left which can be made.
  * ``guesses_made:int`` : The number of guesses_allowed made.
  * ``schema:dict`` : The schema required for the methods ``to_json`` and ``from_json``.
