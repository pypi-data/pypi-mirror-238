"""Tests if  ``empty_array`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/numpy_arrays/test_empty_array.py
    or
    python -m unittest -b tests/numpy_arrays/test_empty_array.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np


### FUNCTION IMPORT ###
from paramcheckup.numpy_arrays import empty_array


os.system('cls')



class Test_empty_array(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.arr = np.array([1, 2, 3])

    def test_outputs(self):
        output = empty_array(self.arr, "param_name", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        output = empty_array(arr=self.arr, param_name="parametro", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")         


    def test_empty_array(self):
        with self.assertRaises(ValueError, msg="Does not raised error when the numpy array is empty"):
            x = np.array([])
            empty_array(x, param_name="param", func_name="func_name") 
   
    def test_correct(self):
        x = np.array([1,2,3,4])
        result = empty_array(x, param_name="param", func_name="func_name") 
        self.assertTrue(result, msg="Does not return True when the input is np.array([1,2,3,4])")




if __name__ == "__main__":
    unittest.main()    