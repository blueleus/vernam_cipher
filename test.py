import unittest
from cipher import random_key, InputError, repeat


class RandomKeyTest(unittest.TestCase):

    def test_return_string(self):
        self.assertIsInstance(random_key(10), str)

    def test_returns_string_with_the_specified_length(self):
        self.assertEqual(len(random_key(30)), 30)

    def test_if_length_is_None_raises_exception(self):
        with self.assertRaises(InputError):
            random_key(None)


class RepeatTest(unittest.TestCase):

    def test_repeat_string_until_length(self):
        self.assertEqual(repeat("test", 10), "testtestte")

    # TODO Test the first parameter is a string
    # TODO Test the second parameter is a integer


if __name__ == "__main__":
    unittest.main()
