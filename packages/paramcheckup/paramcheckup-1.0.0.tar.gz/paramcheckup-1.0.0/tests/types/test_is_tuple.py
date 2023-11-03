"""Tests if  ``is_tuple`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/types/test_is_tuple.py
    or
    python -m unittest -b tests/types/test_is_tuple.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np


### FUNCTION IMPORT ###
from paramcheckup.types import is_tuple


os.system('cls')



class Test_is_tuple(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        pass

    def test_outputs(self):
        output = is_tuple((1,2,3), "parametro", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        output = is_tuple(value=(1,2,3), param_name="parametro", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")        

   

    def test_string(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_tuple("a", param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_tuple("auisdhsa9d8ysadasd9oasdasdonha nsad\n", param_name="param", func_name="func_name")

    def test_float(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_tuple(1.1, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_tuple(1.1012, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_tuple(1.0, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_tuple(np.float32(1), param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is float"):
            is_tuple(np.float64(1), param_name="param", func_name="func_name")

    def test_int(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a int"):
            is_tuple(1, param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a int"):
            is_tuple(np.int64(1), param_name="param", func_name="func_name")

    def test_list(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_tuple([1], param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_tuple([1,1,1], param_name="param", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_tuple([1, (1,), 1], param_name="param", func_name="func_name")

    def test_empty(self):
        with self.assertRaises(TypeError, msg="Does not raised error when no value was passed"):
            is_tuple(param_name="param", func_name="func_name")

    def test_pass(self):
        result = is_tuple((1,), param_name="param", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was (1),")

        result = is_tuple((1, 2, 3), param_name="param", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was (1, 2, 3)")

        result = is_tuple(([1,2,3],), param_name="param", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was ([1,2,3],)")   




if __name__ == "__main__":
    unittest.main()    