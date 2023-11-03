"""Tests if  ``is_between_a_and_b`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/numbers/test_is_between_a_and_b.py
    or
    python -m unittest -b tests/numbers/test_is_between_a_and_b.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest


### FUNCTION IMPORT ###
from paramcheckup.numbers import is_between_a_and_b


os.system('cls')



class Test_is_between_a_and_b(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.value = 1
        cls.a = 0
        cls.b = 2

    def test_outputs(self):
        output = is_between_a_and_b(self.value, self.a, self.b, "param_name", "func_name", True)
        self.assertTrue(output, msg="not True when must be True")
        output = is_between_a_and_b(value=self.value, a=self.a, b=self.b, param_name="param_name", func_name="func_name", inclusive=True)
        self.assertTrue(output, msg="not True when must be True")        


    def test_raises_inclusive_true_reverted(self):

        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = -0.5, 1, 0
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name")            
            

        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = 0.5, -1, 0
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name")


        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = -10.5, -1, 1
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name")

        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = 60.5, -1, 1
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name")
            


    def test_raises_inclusive_true(self):
        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = -0.5, 0, 1
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name")

        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = 0.5, -1, 0
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name")

        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = -10.5, -1, 1
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name")

        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = 60.5, -1, 1
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name")



    def test_raises_inclusive_false(self):
        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = -0.5, 0, 1
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name", inclusive=False)

        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = 0.5, -1, 0
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name", inclusive=False)

        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = -10.5, -1, 1
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name", inclusive=False)

        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = 60.5, -1, 1
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name", inclusive=False)            
            
        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = -1, -1, 1
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name", inclusive=False) 

        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = 1, -1, 1
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name", inclusive=False)                        


    def test_raises_inclusive_false_reverted(self):

        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = -0.5, 1, 0
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name", inclusive=False)            
            

        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = 0.5, -1, 0
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name", inclusive=False)


        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = -10.5, -1, 1
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name", inclusive=False)

        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = 60.5, -1, 1
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name", inclusive=False)
            
        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = -1, 1, -1
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name", inclusive=False) 

        with self.assertRaises(ValueError, msg="Does not raised error when value not in range"):
            value, lower, upper = 1, 1, -1
            result = is_between_a_and_b(value, lower, upper, "param_name", "func_name", inclusive=False)  



    def test_pass_inclusive_true(self):
        value, lower, upper = 0.5, 0, 1
        result = is_between_a_and_b(value, lower, upper, "param_name", "func_name")
        self.assertTrue(result, msg = "Raised error when value in range")

        value, lower, upper = 0.0, 0, 1
        result = is_between_a_and_b(value, lower, upper, "param_name", "func_name")
        self.assertTrue(result, msg = "Raised error when value in range")

        value, lower, upper = 1, 0, 1
        result = is_between_a_and_b(value, lower, upper, "param_name", "func_name")
        self.assertTrue(result, msg = "Raised error when value in range")        


        value, lower, upper = 0.5, -1, 1
        result = is_between_a_and_b(value, lower, upper, "param_name", "func_name")
        self.assertTrue(result, msg = "Raised error when value in range")

        value, lower, upper = -0.5, -1, 1
        result = is_between_a_and_b(value, lower, upper, "param_name", "func_name")
        self.assertTrue(result, msg = "Raised error when value in range")



    def test_pass_inclusive_false(self):
        value, lower, upper = 0.5, 0, 1
        result = is_between_a_and_b(value, lower, upper, "param_name", "func_name", inclusive=False)
        self.assertTrue(result, msg = "Raised error when value in range")



        value, lower, upper = 0.5, -1, 1
        result = is_between_a_and_b(value, lower, upper, "param_name", "func_name", inclusive=False)
        self.assertTrue(result, msg = "Raised error when value in range")

        value, lower, upper = -0.5, -1, 1
        result = is_between_a_and_b(value, lower, upper, "param_name", "func_name", inclusive=False)
        self.assertTrue(result, msg = "Raised error when value in range")        


      



if __name__ == "__main__":
    unittest.main()    