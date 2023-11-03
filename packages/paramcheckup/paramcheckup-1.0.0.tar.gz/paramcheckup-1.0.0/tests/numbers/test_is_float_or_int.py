"""Tests if  ``is_float_or_int`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/numbers/test_is_float_or_int.py
    or
    python -m unittest -b tests/numbers/test_is_float_or_int.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np


### FUNCTION IMPORT ###
from paramcheckup.numbers import is_float_or_int


os.system('cls')



class Test_is_float_or_int(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        pass

    def test_outputs(self):
        output = is_float_or_int(1, "parametro", "func_name")
        self.assertTrue(output, msg="not True when must be True")



    def test_string(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_float_or_int("a", param_name="parameter", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_float_or_int("hausdasuda \n", param_name="parameter", func_name="func_name")

    def test_list(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_float_or_int([1], param_name="parameter", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list of list"):
            is_float_or_int([[1]], param_name="parameter", func_name="func_name")

    def test_tuple(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_float_or_int((1,), param_name="parameter", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_float_or_int((1,1,1), param_name="parameter", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_float_or_int((1, (1,), 1), param_name="parameter", func_name="func_name")

    def test_empty(self):
        with self.assertRaises(TypeError, msg="Does not raised error when no value was passed"):
            is_float_or_int(param_name="parameter", func_name="func_name")

    def test_pass(self):
        result = is_float_or_int(1, param_name="parameter", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was 1")

        result = is_float_or_int(np.int32(1), param_name="parameter", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was np.int32(1)")

        result = is_float_or_int(np.int64(1), param_name="parameter", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was np.int64(1)")

        result = is_float_or_int(np.uint(1), param_name="parameter", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was np.uint(1)")

        result = is_float_or_int(1, param_name="parameter", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was 1")

        result = is_float_or_int(np.int32(1), param_name="parameter", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was np.int32(1)")

        result = is_float_or_int(np.int64(1), param_name="parameter", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was np.int64(1)")

        result = is_float_or_int(np.uint(1), param_name="parameter", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was np.uint(1)")


if __name__ == "__main__":
    unittest.main()    