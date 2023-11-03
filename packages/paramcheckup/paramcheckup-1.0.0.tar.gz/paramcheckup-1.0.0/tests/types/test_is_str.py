"""Tests if  ``is_str`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/types/test_is_str.py
    or
    python -m unittest -b tests/types/test_is_str.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np


### FUNCTION IMPORT ###
from paramcheckup.types import is_str


os.system('cls')



class Test_is_str(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        pass

    def test_outputs(self):
        output = is_str("42", "parametro", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        output = is_str(value="42", param_name="parametro", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")        

   

    def test_int(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is int"):
            is_str(1, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is int"):
            is_str(np.int32(1), param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is int"):
            is_str(np.int64(1), param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is int"):
            is_str(np.uint(1), param_name="param", func_name="func_name")


    def test_float(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_str(1.1, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_str(1.1012, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_str(1.0, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_str(np.float32(1), param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_str(np.float64(1), param_name="param", func_name="func_name")

    def test_list(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_str([1], param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_str([[1]], param_name="param", func_name="func_name")

    def test_tuple(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_str((1,), param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_str((1,1,1), param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_str((1, (1,), 1), param_name="param", func_name="func_name")

    def test_empty(self):
        with self.assertRaises(TypeError, msg="Does not raised error when no value was passed"):
            is_str(param_name="param", func_name="func_name")


    def test_pass(self):
        result = is_str("a", param_name="param", func_name="func_name")
        self.assertTrue(result, msg="Does not returned True with a string")

        result = is_str("auisdhsa9d8ysadasd9oasdasdonha nsad\n", param_name="param", func_name="func_name")
        self.assertTrue(result, msg="Does not returned True with a string")

        result = is_str("", param_name="param", func_name="func_name")
        self.assertTrue(result, msg="Does not returned True when an empty string was passed")        

   



if __name__ == "__main__":
    unittest.main()    