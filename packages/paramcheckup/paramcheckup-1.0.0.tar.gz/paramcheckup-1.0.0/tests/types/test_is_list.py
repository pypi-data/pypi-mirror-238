"""Tests if  ``is_list`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/types/test_is_list.py
    or
    python -m unittest -b tests/types/test_is_list.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np


### FUNCTION IMPORT ###
from paramcheckup.types import is_list


os.system('cls')



class Test_is_list(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        pass

    def test_outputs(self):
        output = is_list([1], "parametro", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        output = is_list(value=[0], param_name="parametro", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")        

   

    def test_string(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_list("a", param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_list("auisdhsa9d8ysadasd9oasdasdonha nsad\n", param_name="param", func_name="func_name")

    def test_float(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_list(1.1, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_list(1.1012, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_list(1.0, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_list(np.float32(1), param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_list(np.float64(1), param_name="param", func_name="func_name")

    def test_int(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_list(1, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_list(np.int64(1), param_name="param", func_name="func_name")

    def test_tuple(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_list((1,), param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_list((1,1,1), param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_list((1, (1,), 1), param_name="param", func_name="func_name")

    def test_empty(self):
        with self.assertRaises(TypeError, msg="Does not raised error when no value was passed"):
            is_list(param_name="param", func_name="func_name")

    def test_pass(self):
        result = is_list([1], param_name="param", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was [1]")

        result = is_list([1, 2, 3], param_name="param", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was [1, 2, 3]")

        result = is_list([[1,2,3]], param_name="param", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was [[1,2,3]]")   




if __name__ == "__main__":
    unittest.main()    