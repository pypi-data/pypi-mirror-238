"""Tests if  ``is_float`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/types/test_is_float.py
    or
    python -m unittest -b tests/types/test_is_float.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np


### FUNCTION IMPORT ###
from paramcheckup.types import is_float


os.system('cls')



class Test_is_float(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        pass

    def test_outputs(self):
        output = is_float(0.1, "parametro", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        output = is_float(value=.1, param_name="parametro", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")        

    def test_string(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_float("a", param_name="parameter", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_float("auisdhsa9d8ysadasd9oasdasdonha nsad\n", param_name="parameter", func_name="func_name")

    def test_int(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is int"):
            is_float(1, param_name="parameter", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is int"):
            is_float(np.int32(1), param_name="parameter", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is int"):
            is_float(np.int64(1), param_name="parameter", func_name="func_name")

    def test_list(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_float([1], param_name="parameter", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_float([[1]], param_name="parameter", func_name="func_name")

    def test_tuple(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_float((1,), param_name="parameter", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_float((1,1,1), param_name="parameter", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_float((1, (1,), 1), param_name="parameter", func_name="func_name")

    def test_empty(self):
        with self.assertRaises(TypeError, msg="Does not raised error when no value was passed"):
            is_float(param_name="parameter", func_name="func_name")

    def test_pass(self):
        result = is_float(1.1, param_name="parameter", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was 1.1")

        result = is_float(np.float32(1), param_name="parameter", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was np.float32(1)")

        result = is_float(np.float64(1), param_name="parameter", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was np.float64(1)")  
  


if __name__ == "__main__":
    unittest.main()    