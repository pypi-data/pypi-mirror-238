"""Tests if  ``is_greater_than`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/numbers/test_is_greater_than.py
    or
    python -m unittest -b tests/numbers/test_is_greater_than.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest


### FUNCTION IMPORT ###
from paramcheckup.numbers import is_greater_than


os.system('cls')



class Test_is_greater_than(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.value = 1
        cls.lower = 0


    def test_outputs(self):
        output = is_greater_than(self.value, self.lower, "param_name", "func_name", True)
        self.assertTrue(output, msg="not True when must be True")
        output = is_greater_than(value=self.value, lower=self.lower, param_name="param_name", func_name="func_name", inclusive=True)
        self.assertTrue(output, msg="not True when must be True")        




    def test_raises_inclusive_true(self):
        with self.assertRaises(ValueError, msg="Does not raised error when value not greater than"):
            value, lower = -0.5, 0
            result = is_greater_than(value, lower, "param_name", "func_name", inclusive=True)

        with self.assertRaises(ValueError, msg="Does not raised error when value not greater than"):
            value, lower = -10.5, -10
            result = is_greater_than(value, lower, "param_name", "func_name", inclusive=True)

        with self.assertRaises(ValueError, msg="Does not raised error when value not greater than"):
            value, lower = 100, 500
            result = is_greater_than(value, lower, "param_name", "func_name", inclusive=True)

        with self.assertRaises(ValueError, msg="Does not raised error when value not greater than"):
            value, lower = 0, 0
            result = is_greater_than(value, lower, "param_name", "func_name", inclusive=True) 

        with self.assertRaises(ValueError, msg="Does not raised error when value not greater than"):
            value, lower = -10, -10
            result = is_greater_than(value, lower, "param_name", "func_name", inclusive=True)                        

        with self.assertRaises(ValueError, msg="Does not raised error when value not greater than"):
            value, lower = 10, 10
            result = is_greater_than(value, lower, "param_name", "func_name", inclusive=True)                        


    def test_raises_inclusive_false(self):
        with self.assertRaises(ValueError, msg="Does not raised error when value not greater than"):
            value, lower = -0.5, 0
            result = is_greater_than(value, lower, "param_name", "func_name", inclusive=False)

        with self.assertRaises(ValueError, msg="Does not raised error when value not greater than"):
            value, lower = -10.5, -10
            result = is_greater_than(value, lower, "param_name", "func_name", inclusive=False)

        with self.assertRaises(ValueError, msg="Does not raised error when value not greater than"):
            value, lower = 100, 500
            result = is_greater_than(value, lower, "param_name", "func_name", inclusive=False)


    def test_pass_inclusive_true(self):
        value, lower = 0.5, 0
        result = is_greater_than(value, lower, "param_name", "func_name", inclusive=True)
        self.assertTrue(result, msg = "Raised error when value in greater than")


        value, lower = 0.5, -.5
        result = is_greater_than(value, lower, "param_name", "func_name", inclusive=True)
        self.assertTrue(result, msg = "Raised error when value in greater than")        


        value, lower = -0.5, -1.5
        result = is_greater_than(value, lower, "param_name", "func_name", inclusive=True)
        self.assertTrue(result, msg = "Raised error when value in greater than")  


    def test_pass_inclusive_false(self):
        value, lower = 0.5, 0
        result = is_greater_than(value, lower, "param_name", "func_name", inclusive=False)
        self.assertTrue(result, msg = "Raised error when value in greater than")


        value, lower = 0.5, -.5
        result = is_greater_than(value, lower, "param_name", "func_name", inclusive=False)
        self.assertTrue(result, msg = "Raised error when value in greater than")        


        value, lower = -0.5, -1.5
        result = is_greater_than(value, lower, "param_name", "func_name", inclusive=False)
        self.assertTrue(result, msg = "Raised error when value in greater than")  

        value, lower = 0.5, 0.5
        result = is_greater_than(value, lower, "param_name", "func_name", inclusive=False)
        self.assertTrue(result, msg = "Raised error when value in greater than")  


      



if __name__ == "__main__":
    unittest.main()    