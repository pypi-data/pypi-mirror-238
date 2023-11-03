"""Tests if  ``is_negative`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/numbers/test_is_negative.py
    or
    python -m unittest -b tests/numbers/test_is_negative.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest


### FUNCTION IMPORT ###
from paramcheckup.numbers import is_negative


os.system('cls')



class Test_is_negative(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        pass

    def test_outputs(self):
        output = is_negative(-1, "parametro", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        output = is_negative(value=-1, param_name="parametro", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")        


    def test_positive(self):
        with self.assertRaises(ValueError, msg="Does not raised error when value is 1"):
            is_negative(1, "param", func_name="func_name")
        with self.assertRaises(ValueError, msg="Does not raised error when value is 0.00000000000001"):
            is_negative(0.00000000000001, "param", func_name="func_name")
        with self.assertRaises(ValueError, msg="Does not raised error when value is 10000000000.111111"):
            is_negative(10000000000.111111, "param", func_name="func_name")


    def test_zero(self):
        with self.assertRaises(ValueError, msg="Does not raised error when value 0"):
            is_negative(0, "param", func_name="func_name")
        with self.assertRaises(ValueError, msg="Does not raised error when value 0"):
            is_negative(0.0, "param", func_name="func_name")

    def test_pass(self):
        result = is_negative(-1, "param", func_name="func_name")
        self.assertTrue(result, msg="Does not returned True when value is 1")

        result = is_negative(-1.00001, "param", func_name="func_name")
        self.assertTrue(result, msg="Does not returned True when value is 1.00001")

        result = is_negative(-0.000000000001, "param", func_name="func_name")
        self.assertTrue(result, msg="Does not returned True when value is 0.000000000001")

        result = is_negative(-1186486464161647, "param", func_name="func_name")
        self.assertTrue(result, msg="Does not returned True when value is 1186486464161647")





if __name__ == "__main__":
    unittest.main()    