import json
import sys
from unittest import TestCase

import jsonschema
from python_digits import DigitWord

from python_cowbull_game.v1_deprecated.GameObject import GameObject


class test_GameObject(TestCase):
    def test_go_instantiation(self):
        go = GameObject()
        self.assertIsNone(go.key)
        self.assertIsNone(go.status)
        self.assertIsNone(go.ttl)
        self.assertIsNone(go.answer)
        self.assertIsNone(go.mode)
        self.assertIsNone(go.guesses_remaining)
        self.assertIsNone(go.guesses_made)

    def test_go_set_key(self):
        go = GameObject()
        go.key = "12-34-56-78-99"
        self.assertEqual(go.key, "12-34-56-78-99")

    def test_go_set_key_bad(self):
        go = GameObject()
        with self.assertRaises(ValueError):
            go.key = None

    def test_go_set_status(self):
        go = GameObject()
        go.status = "playing"
        self.assertEqual(go.status, "playing")

    def test_go_set_status_bad(self):
        go = GameObject()
        with self.assertRaises(ValueError):
            go.status = "playings"

    def test_go_set_ttl(self):
        go = GameObject()
        go.ttl = 120
        self.assertEqual(go.ttl, 120)

    def test_go_set_ttl_bad(self):
        go = GameObject()
        with self.assertRaises(TypeError):
            go.ttl = "120"

    def test_go_set_ttl_low(self):
        go = GameObject()
        with self.assertRaises(ValueError):
            go.ttl = 0

    def test_go_set_answer(self):
        go = GameObject()
        go.answer = DigitWord(1, 2, 3, 4)
        self.assertEqual(go.answer.word, [1, 2, 3, 4])

    def test_go_set_answer_bad(self):
        go = GameObject()
        with self.assertRaises(TypeError):
            go.answer = "playings"

    def test_go_set_answer_bad_dw(self):
        go = GameObject()
        with self.assertRaises(ValueError):
            go.answer = DigitWord("A", 2, "S")

    def test_go_set_mode(self):
        go = GameObject()
        go.mode = "hard"
        self.assertEqual(go.mode, "hard")

    def test_go_set_mode_bad(self):
        go = GameObject()
        with self.assertRaises(ValueError):
            go.mode = "crazy-hard"

    def test_go_set_guesses_remaining(self):
        go = GameObject()
        go.guesses_remaining = 5
        self.assertEqual(go.guesses_remaining, 5)

    def test_go_set_guesses_remaining_bad(self):
        go = GameObject()
        with self.assertRaises(TypeError):
            go.guesses_remaining = "crazy-hard"

    def test_go_set_guesses_remaining_low(self):
        go = GameObject()
        with self.assertRaises(ValueError):
            go.guesses_remaining = -1

    def test_go_set_guesses_made(self):
        go = GameObject()
        go.guesses_made = 5
        self.assertEqual(go.guesses_made, 5)

    def test_go_set_guesses_made_bad(self):
        go = GameObject()
        with self.assertRaises(TypeError):
            go.guesses_made = "crazy-hard"

    def test_go_set_guesses_made_low(self):
        go = GameObject()
        with self.assertRaises(ValueError):
            go.guesses_made = -1

    def test_go_json(self):
        go = GameObject()
        json_string = '{"key": "68b5aea6-0a09-4d60-bed0-43fbf28d1e87", ' \
                      '"guesses_remaining": 10, "guesses_made": 0, "mode": "normal", ' \
                      '"ttl": 1493339159, "status": "playing", "answer": [1, 2, 3, 4]}'
        go.from_json(jsonstr=json_string)
        self.assertEqual(go.key, "68b5aea6-0a09-4d60-bed0-43fbf28d1e87")
        self.assertEqual(go.guesses_remaining, 10)
        self.assertEqual(go.guesses_made, 0)
        self.assertEqual(go.mode, "normal")
        self.assertEqual(go.ttl, 1493339159)
        self.assertEqual(go.status, "playing")
        self.assertEqual(go.answer.word, [1, 2, 3, 4])
        self.assertEqual(len(go.to_json()), len(json_string))   # Compare length because JSON string
                                                                # can be different every time!

    def test_go_json_bad(self):
        go = GameObject()
        json_string = '{"key": null, ' \
                      '"guesses_remaining": 10, "guesses_made": 0, "mode": "normal", ' \
                      '"ttl": 1493339159, "status": "playing", "answer": [1, 2, 3, 4]}'
        json_string2 = '{"skey": "68b5aea6-0a09-4d60-bed0-43fbf28d1e87", ' \
                       '"guesses_remaining": 10, "guesses_made": 0, "mode": "normal", ' \
                       '"ttl": 1493339159, "status": "playing", "answer": [1, 2, 3, 4]}'
        exception_to_check = ValueError
        if sys.version_info[0] > 2:
            exception_to_check = json.decoder.JSONDecodeError
        with self.assertRaises(exception_to_check):
            go.from_json(jsonstr='')
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            go.from_json(jsonstr=json_string)
        with self.assertRaises(KeyError):
            go.from_json(jsonstr=json_string2)
