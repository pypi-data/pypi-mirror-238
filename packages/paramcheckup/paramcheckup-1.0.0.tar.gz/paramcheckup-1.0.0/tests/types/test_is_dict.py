"""Tests if  ``is_dict`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/types/test_is_dict.py
    or
    python -m unittest -b tests/types/test_is_dict.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np


### FUNCTION IMPORT ###
from paramcheckup.types import is_dict


os.system('cls')



class Test_is_dict(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.dicionario = {"A": 1,}

    def test_outputs(self):
        output = is_dict(self.dicionario, "parametro", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        output = is_dict(value=self.dicionario, param_name="parametro", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")        

 
 
    def test_string(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_dict("a", param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_dict("auisdhsa9d8ysadasd9oasdasdonha nsad\n", param_name="param", func_name="func_name")

    def test_float(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_dict(1.1, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_dict(1.1012, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_dict(1.0, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_dict(np.float32(1), param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_dict(np.float64(1), param_name="param", func_name="func_name")

    def test_int(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_dict(1, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_dict(np.int64(1), param_name="param", func_name="func_name")

    def test_tuple(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_dict((1,), param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_dict((1,1,1), param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_dict((1, (1,), 1), param_name="param", func_name="func_name")

    def test_empty(self):
        with self.assertRaises(TypeError, msg="Does not raised error when no value was passed"):
            is_dict(param_name="param", func_name="func_name")

    def test_pass(self):

        result = is_dict({"a": 1}, param_name="param", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was {'a': 1}")

        result = is_dict({"a": 1, "b": 2}, param_name="param", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was {'a': 1, 'b': 2}")

        result = is_dict({"a": [1]}, param_name="param", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was {'a': [1]}")

        result = is_dict({"a": [1,2,3], "b": "2"}, param_name="param", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was {'a': [1,2,3], 'b': '2'}")






if __name__ == "__main__":
    unittest.main()    