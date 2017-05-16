# python_cowbull_game
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

``
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
``



The objective behind this project is to provide a Python function which provides an object
to represent a digit (an integer between 0 (zero) and 9 (nine)). This is further extended
by providing an object (a DigitWord) which represents a collection of Digits, in a set
sequence (e.g. 0421 would be a DigitWord with a length of 4 and containing 4 digits of the
values: 0, 4, 2, and 1.)

The reason I created this package is for a cowbull game I have been developing which allows
a series of digits to be randomly generated and then for a user to guess each digit.
If the guessed digit is in the right place, then it's a bull; if the guessed digit is in
the wrong place, then it's a cow.

To aid this, the DigitWord allows comparisons of multiple DigitWords and returns a list of
DigitWordAnalysis (DWA) objects.  The DWA objects state the index (the position of the
guessed digit), the digit (the guess, not the actual digit), a match (True or False) indicator,
an in word (True or False) indicator, and a multiple (True or False) indicator which shows
whether the guessed number actually occurred more than once.

## Installation
After forking this repository (or cloning using https), the package can be installed typing

```pip install .```

and will then be available to your Python environment. Virtualenv is recommended to avoid polluting your
Python environment. The Python package is also available at
https://pypi.python.org/pypi?name=python-digits&:action=display and can be installed using
pip:

```pip install python_digits```

## Tests
When installing the package from source, tests are held in a directory called (unsurprisingly) tests.
To validate the package, run the tests as follows from the installation directory:

```python -m unittest python_digits.tests```

Add new tests into new files in the tests directory and update __init__.py to import them, then
tests can be run using the command above. *Hint* Use -v python_digits.tests to see the test results
in verbose mode.

## Usage
To use the package, do the following steps:

```
$ python
>>> from python_digits import Digit, DigitWord, DigitWordAnalysis
>>> d = Digit(0) # Creates a digit 0
>>> de = Digit(22) # Raises a ValueError
>>> dw1 = DigitWord() # Creates an *empty* DigitWord
>>> dw2 = DigitWord(1, 4, 7, 2) # Creates a DigitWord containing 1, 4, 7, and 2.
>>> dw3 = DigitWord(4, 1, 8, 0) # Creates a DigitWord containing 4, 1, 8, and 0.
>>> str(dw2) # Returns '1472'
>>> dw2.word # Returns [1, 4, 7, 2]
>>> dw2.compare(dw3) # Returns a list of DigitWordAnalysis objects
```
Try the following code to see what the objects contain:
```
>>> for i in dw2.compare(dw3):
...     print(i.index, i.digit, i.match, i.in_word, i.multiple)
#
# The results should be
#
# 0 4 False True False
# 1 1 False True False
# 2 8 False False False
# 3 0 False False False
#
```
Equality can also be compared. Try the following:
```
>>> dw4 = DigitWord(1, 2, 3, 4, 5, 6)
>>> dw5 = DigitWord(1, 2, 3, 4, 5, 6)
>>> dw6 = DigitWord(1, 2)
>>> dw7 = DigitWord(6, 5, 4, 3, 2, 1)
>>> dw4 == dw5 # Returns True
>>> dw4 == dw6 # Returns False
>>> dw5 == dw7 # Returns False
```
Empty DigitWords can be set to contain a random word:
```
>>> dw = DigitWord() # Empty DigitWord
>>> dw.random(5) # Create a random word with 5 digits
>>> dw.word # Returns a list of the digits created by the random method
```
An end-to-end example is provided below:
```
>>> from python_digits import Digit, DigitWord
>>> dw = DigitWord()
>>> dw.random(4)
>>> analysis = dw.compare(DigitWord(1, 2, 3, 4))
>>> for a in analysis:
...     print(a.get_object())
```
## Digit class
Digit - a **subclass** of int designed to store a single digit between 0 and 9. A Digit is
formed by instantiation and passing integers (or string representation) using the parameter
value. The value must be between 0 and 9 (e.g. 0, 1, 2, 3, 4, 5, 6, 7, 8, or 9) and will
raise a ValueError if not. As a subclass of int, the Digit class obeys all integer operations
such as multiply, add, etc.

* Instantiation: ```obj = Digit(value:int)```
* Methods: ```None```
* Properties: ```None```


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
