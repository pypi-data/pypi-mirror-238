"""Tests if  ``is_int`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/types/test_is_int.py
    or
    python -m unittest -b tests/types/test_is_int.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np


### FUNCTION IMPORT ###
from paramcheckup.types import is_int


os.system('cls')



class Test_is_int(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        pass

    def test_outputs(self):
        output = is_int(1, "parametro", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        output = is_int(value=0, param_name="parametro", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")        

   

    def test_string(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_int("a", param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_int("auisdhsa9d8ysadasd9oasdasdonha nsad\n", param_name="param", func_name="func_name")

    def test_float(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_int(1.1, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_int(1.1012, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_int(1.0, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_int(np.float32(1), param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_int(np.float64(1), param_name="param", func_name="func_name")

    def test_list(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_int([1], param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_int([[1]], param_name="param", func_name="func_name")

    def test_tuple(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_int((1,), param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_int((1,1,1), param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_int((1, (1,), 1), param_name="param", func_name="func_name")

    def test_empty(self):
        with self.assertRaises(TypeError, msg="Does not raised error when no value was passed"):
            is_int(param_name="param", func_name="func_name")

    def test_pass(self):
        result = is_int(1, param_name="param", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was 1")

        result = is_int(np.int32(1), param_name="param", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was np.int32(1)")

        result = is_int(np.int64(1), param_name="param", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was np.int64(1)")

        result = is_int(np.uint(1), param_name="param", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was np.uint(1)")
   



if __name__ == "__main__":
    unittest.main()    