"""Tests if  ``is_lower_than`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/numbers/test_is_lower_than.py
    or
    python -m unittest -b tests/numbers/test_is_lower_than.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest


### FUNCTION IMPORT ###
from paramcheckup.numbers import is_lower_than


os.system('cls')



class Test_is_lower_than(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.value = 0
        cls.upper = 1


    def test_outputs(self):
        output = is_lower_than(self.value, self.upper, "param_name", "func_name", True)
        self.assertTrue(output, msg="not True when must be True")
        output = is_lower_than(value=self.value, upper=self.upper, param_name="param_name", func_name="func_name", inclusive=True)
        self.assertTrue(output, msg="not True when must be True")        




    def test_raises_inclusive_true(self):
        with self.assertRaises(ValueError, msg="Does not raised error when value not lower than"):
            value, upper = 0, -0.5
            result = is_lower_than(value, upper, "param_name", "func_name", inclusive=True)

        with self.assertRaises(ValueError, msg="Does not raised error when value not lower than"):
            value, upper = -10, -10.5
            result = is_lower_than(value, upper, "param_name", "func_name", inclusive=True)

        with self.assertRaises(ValueError, msg="Does not raised error when value not lower than"):
            value, upper = 100, 5
            result = is_lower_than(value, upper, "param_name", "func_name", inclusive=True)

        with self.assertRaises(ValueError, msg="Does not raised error when value not lower than"):
            value, upper = 0, 0
            result = is_lower_than(value, upper, "param_name", "func_name", inclusive=True)

        with self.assertRaises(ValueError, msg="Does not raised error when value not lower than"):
            value, upper = -10, -10
            result = is_lower_than(value, upper, "param_name", "func_name", inclusive=True)

        with self.assertRaises(ValueError, msg="Does not raised error when value not lower than"):
            value, upper = 10, 10
            result = is_lower_than(value, upper, "param_name", "func_name", inclusive=True)


    def test_raises_inclusive_false(self):
        with self.assertRaises(ValueError, msg="Does not raised error when value not lower than"):
            value, upper = 0, -0.5
            result = is_lower_than(value, upper, "param_name", "func_name", inclusive=False)

        with self.assertRaises(ValueError, msg="Does not raised error when value not lower than"):
            value, upper = -10, -10.5
            result = is_lower_than(value, upper, "param_name", "func_name", inclusive=False)

        with self.assertRaises(ValueError, msg="Does not raised error when value not lower than"):
            value, upper = 100, 5
            result = is_lower_than(value, upper, "param_name", "func_name", inclusive=False)


    def test_pass_inclusive_true(self):
        value, upper = 0, 0.5
        result = is_lower_than(value, upper, "param_name", "func_name", inclusive=True)
        self.assertTrue(result, msg = "Raised error when value in lower than")


        value, upper = -.5, 0.5
        result = is_lower_than(value, upper, "param_name", "func_name", inclusive=True)
        self.assertTrue(result, msg = "Raised error when value in lower than")        


        value, upper = -1.5, -0.5
        result = is_lower_than(value, upper, "param_name", "func_name", inclusive=True)
        self.assertTrue(result, msg = "Raised error when value in lower than")  


    def test_pass_inclusive_false(self):
        value, upper = 0, 0.5
        result = is_lower_than(value, upper, "param_name", "func_name", inclusive=False)
        self.assertTrue(result, msg = "Raised error when value in lower than")


        value, upper = -.5, 0.5
        result = is_lower_than(value, upper, "param_name", "func_name", inclusive=False)
        self.assertTrue(result, msg = "Raised error when value in lower than")        


        value, upper = -1.5, -0.5
        result = is_lower_than(value, upper, "param_name", "func_name", inclusive=False)
        self.assertTrue(result, msg = "Raised error when value in lower than")  

        value, upper = 0.5, 0.5
        result = is_lower_than(value, upper, "param_name", "func_name", inclusive=False)
        self.assertTrue(result, msg = "Raised error when value in lower than")  


      



if __name__ == "__main__":
    unittest.main()    