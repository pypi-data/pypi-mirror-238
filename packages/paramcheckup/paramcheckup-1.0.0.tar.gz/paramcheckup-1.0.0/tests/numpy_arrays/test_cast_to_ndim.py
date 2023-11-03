"""Tests if  ``cast_to_ndim`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/numpy_arrays/test_cast_to_ndim.py
    or
    python -m unittest -b tests/numpy_arrays/test_cast_to_ndim.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np
import pandas as pd

### FUNCTION IMPORT ###
from paramcheckup.numpy_arrays import cast_to_ndim


os.system('cls')



class Test_cast_to_ndim(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.arr = [1, 2, 3]

    def test_outputs(self):
        output = cast_to_ndim(self.arr, "param_name", "func_name", 1)
        self.assertTrue(np.allclose(output, np.array(self.arr)), msg="arrays does not match")


        output = cast_to_ndim(array=self.arr, param_name="param_name", func_name="func_name", ndim=1)
        self.assertTrue(np.allclose(output, np.array(self.arr)), msg="arrays does not match")


    def test_raises_n_dim(self):
        with self.assertRaises(ValueError, msg="Does not raised error when wrong dim"):
            y = [1,2,3,4]
            cast_to_ndim(y, "param_name", "func_name", 2)


        with self.assertRaises(ValueError, msg="Does not raised error when wrong dim"):
            y = [[1,2,3,4]]
            cast_to_ndim(y, "param_name", "func_name", 1)

      
    def test_abc(self):
        with self.assertRaises(ValueError, msg="Does not raised error when dict"):
            x = {"abc": [1,2,3,4]}
            cast_to_ndim(x, "param_name", "func_name")

        with self.assertRaises(ValueError, msg="Does not raised error when set"):
            x = set([1,2,3])
            cast_to_ndim(x, "param_name", "func_name")


        with self.assertRaises(ValueError, msg="Does not raised error when dataframe"):
            cast_to_ndim(x, "param_name", "func_name")
            x = pd.DataFrame({
                "a": [1,2,3]
            })
        with self.assertRaises(ValueError, msg="Does not raised error when dataframe two columns"):
            x = pd.DataFrame({
                "a": [1,2,3],
                "aa": [1,2,3],
            })
            cast_to_ndim(x, "param_name", "func_name")



    def test_raises_zero_dim(self):
        with self.assertRaises(ValueError, msg="Does not raised error when zero dim"):
            y = 1
            x = np.array([1])
            output = cast_to_ndim(y, "param_name", "func_name", 1)
            self.assertTrue(np.allclose(x, output), msg="arrays does not match")             

        with self.assertRaises(ValueError, msg="Does not raised error when zero dim"):
            y = .1
            x = np.array([.1])
            output = cast_to_ndim(y, "param_name", "func_name", 1)
            self.assertTrue(np.allclose(x, output), msg="arrays does not match")                     

        with self.assertRaises(ValueError, msg="Does not raised error when zero dim"):
            y = ".1"
            x = np.array([".1"])
            output = cast_to_ndim(y, "param_name", "func_name", 1)
            self.assertTrue(np.allclose(x, output), msg="arrays does not match")                             

   
    def test_correct(self):
        y = [1,2,3,4]
        x = np.array([1,2,3,4])
        output = cast_to_ndim(y, "param_name", "func_name", 1)
        self.assertTrue(np.allclose(x, output), msg="arrays does not match")

        y = (1,2,3,4)
        x = np.array([1,2,3,4])
        output = cast_to_ndim(y, "param_name", "func_name", 1)
        self.assertTrue(np.allclose(x, output), msg="arrays does not match")      

        y = pd.Series([1,2,3,4])
        x = np.array([1,2,3,4])
        output = cast_to_ndim(y, "param_name", "func_name", 1)
        self.assertTrue(np.allclose(x, output), msg="arrays does not match")      


        y = (1,)
        x = np.array([1])
        output = cast_to_ndim(y, "param_name", "func_name", 1)
        self.assertTrue(np.allclose(x, output), msg="arrays does not match")                


        y = [[1, 4, 9, 16, 25, 36]]
        x = np.array([[1, 4, 9, 16, 25, 36]])
        output = cast_to_ndim(y, "param_name", "func_name", 2)
        self.assertTrue(np.allclose(x, output), msg="arrays does not match")


        y = [[1, 4, 9, 16, 25, 36], [1, 4, 9, 16, 25, 36],]
        x = np.array([[1, 4, 9, 16, 25, 36], [1, 4, 9, 16, 25, 36],])
        output = cast_to_ndim(y, "param_name", "func_name", 2)
        self.assertTrue(np.allclose(x, output), msg="arrays does not match")        



        





if __name__ == "__main__":
    unittest.main()    