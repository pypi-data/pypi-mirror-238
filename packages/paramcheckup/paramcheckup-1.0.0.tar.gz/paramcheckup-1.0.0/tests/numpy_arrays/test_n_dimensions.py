"""Tests if  ``n_dimensions`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/numpy_arrays/test_n_dimensions.py
    or
    python -m unittest -b tests/numpy_arrays/test_n_dimensions.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np


### FUNCTION IMPORT ###
from paramcheckup.numpy_arrays import n_dimensions


os.system('cls')



class Test_integer(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.arr = np.array([1, 2, 3])

    def test_outputs(self):
        output = n_dimensions(self.arr, "param_name", "func_name", 1)
        self.assertTrue(output, msg="not True when must be True")
        output = n_dimensions(arr=self.arr, param_name="parametro", func_name="func_name", n_dimensions=1)
        self.assertTrue(output, msg="not True when must be True")        

   
    def test_two_dimension(self):
        with self.assertRaises(ValueError, msg="Does not raised error when value has 2 dimensions"):
            x = np.array([[1,2,3,4]])
            n_dimensions(x, param_name="param", func_name="func_name", n_dimensions=1)


    def test_correct(self):
        x = np.array([1,2,3,4])
        result = n_dimensions(x, param_name="param", func_name="func_name", n_dimensions=1)
        self.assertTrue(result, msg="Does not return True when the input is np.array([1,2,3,4])")

        x = np.array([[1,2,3,4]])
        result = n_dimensions(x, param_name="param", func_name="func_name", n_dimensions=2)
        self.assertTrue(result, msg="Does not return True when the input is np.array([[1,2,3,4]])")        



if __name__ == "__main__":
    unittest.main()    