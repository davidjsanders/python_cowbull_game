import jsonschema
from time import time
from unittest import TestCase

from python_digits import DigitWord
from ..Game import Game


class test_Game(TestCase):
    def setUp(self):
        self.go = Game()

    def test_game_instantiation(self):
        self.assertIsInstance(self.go, Game)

    def test_game_new_game(self):
        key = self.go.new_game()
        self.assertIsInstance(key, str)

    def test_game_guess_lost(self):
        json_string = '{"key": "68b5aea6-0a09-4d60-bed0-43fbf28d1e87", ' \
                      '"guesses_remaining": 2, "guesses_made": 0, "mode": "normal", ' \
                      '"ttl": ' + str(int(time()) + 3600) + ', "status": "playing", "answer": [1, 2, 3, 4]}'
        self.go.load_game(jsonstr=json_string)

        return_object = self.go.guess(4, 3, 2, 1)
        self.assertEqual(return_object["cows"], 4)
        self.assertEqual(return_object["bulls"], 0)

        return_object = self.go.guess(3, 2, 1, 4)
        self.assertEqual(return_object["cows"], 2)
        self.assertEqual(return_object["bulls"], 2)

        return_object = self.go.guess(2, 1, 4, 3)

    def test_game_save_load_game(self):
        self.go.new_game()
        save_str = self.go.save_game()
        go2 = Game()
        go2.load_game(jsonstr=save_str)
