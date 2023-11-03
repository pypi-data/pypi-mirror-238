"""Tests if  ``matching_size`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/numpy_arrays/test_matching_size.py
    or
    python -m unittest -b tests/numpy_arrays/test_matching_size.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np


### FUNCTION IMPORT ###
from paramcheckup.numpy_arrays import matching_size


os.system('cls')



class Test_matching_size(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.array_a = np.array([1, 2, 3])
        cls.array_b = np.array([1, 2, 3])

    def test_outputs(self):
        output = matching_size(self.array_a, "param_name_a", self.array_b, "param_name_b", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        output = matching_size(array_a=self.array_a, param_name_a="param_name_a", array_b=self.array_b, param_name_b="param_name_b", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")        


    def test_pass(self):
        x1 = np.array([1, 3, 5, 4])
        x2 = np.array([4, 6, 7, 8])
        self.assertTrue(matching_size(x1, "param_name_a", x2, "param_name_b", "func_name"), msg="not True when must be True")

        x1 = np.array([1, 3, 5, 4])
        x2 = np.array(["4", "6", "7", "8"])
        self.assertTrue(matching_size(x1, "param_name_a", x2, "param_name_b", "func_name"), msg="not True when must be True")        

        x1 = np.array(["1", "3", "5", "4"])
        x2 = np.array(["4", "6", "7", "8"])
        self.assertTrue(matching_size(x1, "param_name_a", x2, "param_name_b", "func_name"), msg="not True when must be True")                


    def test_raises_sizes_differ(self):
        with self.assertRaises(ValueError, msg="Does not raised error when the sizes doesn't match"):
            x1 = np.array([1, 3, 5, 4, 4])
            x2 = np.array([4, 6, 7, 8])
            matching_size(x1, "param_name_a", x2, "param_name_b", "func_name")

        with self.assertRaises(ValueError, msg="Does not raised error when the sizes doesn't match"):
            x1 = np.array([1, 3, 5, 4, 4])
            x2 = np.array([4, 6, 7, 8, 5, 6, 8])
            matching_size(x1, "param_name_a", x2, "param_name_b", "func_name")            


if __name__ == "__main__":
    unittest.main()    