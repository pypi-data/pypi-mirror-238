"""Tests if  ``greater_than_n`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/numpy_arrays/test_greater_than_n.py
    or
    python -m unittest -b tests/numpy_arrays/test_greater_than_n.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np


### FUNCTION IMPORT ###
from paramcheckup.numpy_arrays import greater_than_n


os.system('cls')



class Test_cast_greater_than_n(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.x_exp = np.array([1, 2, 3])
        cls.minimum = 3

    def test_outputs(self):
        output = greater_than_n(self.x_exp, "x_exp", "fit", 3, True)
        self.assertTrue(output, msg="not True when it should")

        output = greater_than_n(array=self.x_exp, param_name="x_exp", func_name="fit", minimum=3, inclusive=True)
        self.assertTrue(output, msg="not True when it should")



      
    def test_raises_inclusive_true(self):
        with self.assertRaises(ValueError, msg="Does not raised size is lower than expected"):
            x = np.array([1, 1, 1, 1, 1])
            minimum = 6
            output = greater_than_n(x, "x_exp", "fit", minimum=minimum, inclusive=True)

        with self.assertRaises(ValueError, msg="Does not raised size is lower than expected"):
            x = np.array([1, 1])
            output = greater_than_n(x, "x_exp", "fit", inclusive=True)
            self.assertTrue(output, msg="not True when it should")

                     
    def test_raises_inclusive_true(self):
        with self.assertRaises(ValueError, msg="Does not raised size is lower than expected"):
            x = np.array([1, 1, 1, 1, 1])
            minimum = 5
            output = greater_than_n(x, "x_exp", "fit", minimum=minimum, inclusive=False)
            self.assertTrue(output, msg="not True when it should")

        with self.assertRaises(ValueError, msg="Does not raised size is lower than expected"):
            x = np.array([1, 1, 1])
            output = greater_than_n(x, "x_exp", "fit", minimum=3, inclusive=False)
            self.assertTrue(output, msg="not True when it should")   



    def test_inclusive_true(self):
        x = np.array([1, 1, 1, 1, 1])
        minimum = 5
        output = greater_than_n(x, "x_exp", "fit", minimum=minimum, inclusive=True)
        self.assertTrue(output, msg="not True when it should")

        x = np.array([1, 1, 1])
        output = greater_than_n(x, "x_exp", "fit", inclusive=True)
        self.assertTrue(output, msg="not True when it should")


    def test_inclusive_false(self):
        x = np.array([1, 1, 1, 1, 1])
        minimum = 4
        output = greater_than_n(x, "x_exp", "fit", minimum=minimum, inclusive=False)
        self.assertTrue(output, msg="not True when it should")

        x = np.array([1, 1, 1])
        output = greater_than_n(x, "x_exp", "fit", minimum=2, inclusive=False)
        self.assertTrue(output, msg="not True when it should")



if __name__ == "__main__":
    unittest.main()    