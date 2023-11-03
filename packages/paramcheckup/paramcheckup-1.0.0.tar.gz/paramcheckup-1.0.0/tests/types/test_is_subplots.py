"""Tests if  ``is_subplots`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/types/test_is_subplots.py
    or
    python -m unittest -b tests/types/test_is_subplots.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np
import matplotlib.pyplot as plt

### FUNCTION IMPORT ###
from paramcheckup.types import is_subplots


os.system('cls')



class Test_is_subplots(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        pass

    def test_outputs(self):
        fig, ax = plt.subplots()
        output = is_subplots(ax, "parametro", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        plt.close()

        fig, ax = plt.subplots()
        output = is_subplots(value=ax, param_name="parametro", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")        
        plt.close()

    def test_string(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_subplots("a", param_name="parameter", func_name="func_name")
            plt.close()
        with self.assertRaises(TypeError, msg="Does not raised error when value is a string"):
            is_subplots("auisdhsa9d8ysadasd9oasdasdonha nsad\n", param_name="parameter", func_name="func_name")
            plt.close()

    def test_int(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is int"):
            is_subplots(1, param_name="parameter", func_name="func_name")
            plt.close()
        with self.assertRaises(TypeError, msg="Does not raised error when value is int"):
            is_subplots(np.int32(1), param_name="parameter", func_name="func_name")
            plt.close()
        with self.assertRaises(TypeError, msg="Does not raised error when value is int"):
            is_subplots(np.int64(1), param_name="parameter", func_name="func_name")
            plt.close()

    def test_list(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_subplots([1], param_name="parameter", func_name="func_name")
            plt.close()
        with self.assertRaises(TypeError, msg="Does not raised error when value is a list"):
            is_subplots([[1]], param_name="parameter", func_name="func_name")
            plt.close()

    def test_tuple(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_subplots((1,), param_name="parameter", func_name="func_name")
            plt.close()
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_subplots((1,1,1), param_name="parameter", func_name="func_name")
            plt.close()
        with self.assertRaises(TypeError, msg="Does not raised error when value is a tuple"):
            is_subplots((1, (1,), 1), param_name="parameter", func_name="func_name")
            plt.close()

    def test_empty(self):
        with self.assertRaises(TypeError, msg="Does not raised error when no value was passed"):
            is_subplots(param_name="parameter", func_name="func_name")
            plt.close()

    def test_None(self):
        with self.assertRaises(TypeError, msg="Does not raised error when value is None"):
            is_subplots(None, param_name="parameter", func_name="func_name")
            plt.close()

    def test_pass(self):

        fig, ax = plt.subplots()

        result = is_subplots(ax, param_name="parameter", func_name="func_name")
        self.assertTrue(result, msg = "An error was raised when value was True")
        plt.close()


if __name__ == "__main__":
    unittest.main()    