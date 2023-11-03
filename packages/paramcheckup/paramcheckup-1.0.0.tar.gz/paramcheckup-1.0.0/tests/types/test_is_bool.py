"""Tests if  ``is_bool`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/types/test_is_bool.py
    or
    python -m unittest -b tests/types/test_is_bool.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np


### FUNCTION IMPORT ###
from paramcheckup.types import is_bool


os.system('cls')



class Test_boolean(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        pass

    def test_outputs(self):
        output = is_bool(False, "parametro", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        output = is_bool(value=False, param_name="parametro", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")        

    def test_string(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_bool("a", param_name="parameter", func_name="my_function")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_bool("auisdhsa9d8ysadasd9oasdasdonha nsad\n", param_name="parameter", func_name="my_function")

    def test_int(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is int"):
            is_bool(1, param_name="parameter", func_name="my_function")
        with self.assertRaises(TypeError, msg="Does not raised error when value is int"):
            is_bool(np.int32(1), param_name="parameter", func_name="my_function")
        with self.assertRaises(TypeError, msg="Does not raised error when value is int"):
            is_bool(np.int64(1), param_name="parameter", func_name="my_function")

    def test_list(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_bool([1], param_name="parameter", func_name="my_function")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_bool([[1]], param_name="parameter", func_name="my_function")

    def test_tuple(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_bool((1,), param_name="parameter", func_name="my_function")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_bool((1,1,1), param_name="parameter", func_name="my_function")
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_bool((1, (1,), 1), param_name="parameter", func_name="my_function")

    def test_empty(self):
        with self.assertRaises(TypeError, msg="Does not raised error when no value was passed"):
            is_bool(param_name="parameter", func_name="my_function")

    def test_None(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is None"):
            is_bool(None, param_name="parameter", func_name="my_function")




if __name__ == "__main__":
    unittest.main()    