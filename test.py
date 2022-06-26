import unittest
import os
from unittest import skip
from unittest.mock import patch
from cipher import random_key, InputError, repeat, main, algorithm


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

    def test_repeat_integer_until_length(self):
        self.assertEqual(repeat(1, 10), "1111111111")

    def test_the_second_parameter_must_be_a_integer(self):
        with self.assertRaises(InputError) as cm:
            repeat("test", "10")
        exception = cm.exception
        self.assertEqual(str(exception), "The length parameter must be an integer")


class MainFunctionTest(unittest.TestCase):

    # call to algorithm function with operation_type, file_name, key, verbose
    @patch('cipher.sys')
    @patch('cipher.algorithm')
    def test_call_algorithm_function(self, mock_algorithm, mock_sys):
        mock_sys.argv = ["", "-f", "test_f", "-p", "test_p", "-o", "test_o"]
        main()
        self.assertEqual(mock_algorithm.called, True)
        (file_name, operation_type, key, verbose), kwargs = mock_algorithm.call_args
        self.assertEqual(operation_type, "test_o")
        self.assertEqual(file_name, "test_f")
        self.assertEqual(key, "test_p")


class AlgorithmFunctionTest(unittest.TestCase):
    TEXT_TO_CIPHER = "HELLO"
    TEXT_TO_DECIPHER = "24 9 25 24 0"
    KEY = "PLUTO"

    def setUp(self) -> None:
        with open("file_to_cipher.txt", "w") as f:
            f.write(self.TEXT_TO_CIPHER)

        with open("file_to_decipher.txt", "w") as f:
            f.write(self.TEXT_TO_DECIPHER)

    def tearDown(self) -> None:
        files_to_remove = [
            "file_to_cipher.txt",
            "file_to_decipher.txt",
            "result_cipher.txt",
            "result_decipher.txt"
        ]
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)

    def test_file_name_is_required(self):
        with self.assertRaises(InputError) as cm:
            algorithm(None)
        exception = cm.exception
        self.assertEqual(str(exception), "The file_name parameter is required")

    # cipher operation generate a file named result_cipher.txt
    def test_cipher_operation_generate_a_file_named_result_cipher(self):
        algorithm("file_to_cipher.txt", "cipher")
        self.assertTrue(os.path.exists("result_cipher.txt"))

    # decipher operation generate a file named result_decipher.txt
    def test_decipher_operation_generate_a_file_named_result_decipher(self):
        algorithm("file_to_decipher.txt", "decipher")
        self.assertTrue(os.path.exists("result_decipher.txt"))

    # cipher is the default operation
    def default_operation_is_cipher(self):
        algorithm("file_to_cipher.txt")
        self.assertTrue(os.path.exists("result_cipher.txt"))

    # only .txt file can be operated and return the messaje `The indicated parameter isn't a file`
    def test_validation_when_file_name_parameter_is_not_a_txt_file_name(self):
        with self.assertRaises(ValueError) as cm:
            algorithm("file_to_cipher")
        exception = cm.exception
        self.assertEqual(str(exception), "The file_name parameter must be a .txt file name")

    # cipher operation type
    def test_validation_for_cipher_result(self):
        algorithm("file_to_cipher.txt", key=self.KEY)
        if os.path.exists("result_cipher.txt"):
            content = None
            with open("result_cipher.txt", "r") as f:
                content = f.read()
            self.assertEqual(content, self.TEXT_TO_DECIPHER)

    # decipher operation type
    def test_validation_for_decipher_result(self):
        algorithm("file_to_decipher.txt", operation_type="decipher", key=self.KEY)
        if os.path.exists("result_decipher.txt"):
            content = None
            with open("result_decipher.txt", "r") as f:
                content = f.read()
            self.assertEqual(content, self.TEXT_TO_CIPHER)


if __name__ == "__main__":
    unittest.main()
