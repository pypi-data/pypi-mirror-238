"""Tests if  ``is_numpy`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/types/test_is_numpy.py
    or
    python -m unittest -b tests/types/test_is_numpy.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np
import pandas as pd

### FUNCTION IMPORT ###
from paramcheckup.types import is_numpy


os.system('cls')



class Test_is_numpy(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.data = np.array([1,2,3])

    def test_outputs(self):
        output = is_numpy(self.data, "parametro", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        output = is_numpy(value=self.data, param_name="parametro", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")        


    def test_is_list(self):
        with self.assertRaises(TypeError, msg="Does not raised error when is list"):
            x = [1,2,3,4]
            is_numpy(x, param_name="param", func_name="func_name")

    def test_is_tuple(self):
        with self.assertRaises(TypeError, msg="Does not raised error when is tuple"):
            x = (1,2,3,4)
            is_numpy(x, param_name="param", func_name="func_name")            

    def test_is_dict(self):
        with self.assertRaises(TypeError, msg="Does not raised error when is dict"):
            x = {"a": self.data}
            is_numpy(x, param_name="param", func_name="func_name")                

    def test_is_pandas_series(self):
        with self.assertRaises(TypeError, msg="Does not raised error when is pandas_series"):
            x = pd.Series([1, 2, 3])
            is_numpy(x, param_name="param", func_name="func_name")                                    


    def test_correct(self):
        x = np.array([1,2,3,4])
        result = is_numpy(x, param_name="param", func_name="func_name")
        self.assertTrue(result, msg="Does not return True when the input is np.array([1,2,3,4])")




if __name__ == "__main__":
    unittest.main()    