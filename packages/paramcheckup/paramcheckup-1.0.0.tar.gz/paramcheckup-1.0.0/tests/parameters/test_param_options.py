"""Tests if  ``param_options`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/parameters/test_param_options.py
    or
    python -m unittest -b tests/parameters/test_param_options.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest


### FUNCTION IMPORT ###
from paramcheckup.parameters import param_options


os.system('cls')



class Test_param_options(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.option = "a"
        cls.options = ["a", "b", "c"]
        cls.params = [1, "1", False, [False], {True}, (1,1,1),]

    def test_outputs(self):
        output = param_options(self.option, self.options, "param_name", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        output = param_options(option=self.option, param_options=self.options, param_name="param_name", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")        


    def test_raises(self):
        
        with self.assertRaises(ValueError, msg="Does not raised error param NOT in params_options"):
            result = param_options(0.1, self.params, "param_name", "func_name")

        with self.assertRaises(ValueError, msg="Does not raised error param NOT in params_options"):
            result = param_options("blom", self.params, "param_name", "func_name")

        with self.assertRaises(ValueError, msg="Does not raised error param NOT in params_options"):
            result = param_options(["blom"], self.params, "param_name", "func_name")



    def test_pass(self):
        params = [1, "1", False, [False], {True}, (1,1,1),]
        result = param_options(1, params, "param_name", "func_name")
        self.assertTrue(result, msg="raised error when option in param_options")

        result = param_options("1", params, "param_name", "func_name")
        self.assertTrue(result, msg="raised error when option in param_options")

        result = param_options(False, params, "param_name", "func_name")
        self.assertTrue(result, msg="raised error when option in param_options")

        result = param_options([False], params, "param_name", "func_name")
        self.assertTrue(result, msg="raised error when option in param_options")        

        result = param_options({True}, params, "param_name", "func_name")
        self.assertTrue(result, msg="raised error when option in param_options")        

        result = param_options((1,1,1), params, "param_name", "func_name")
        self.assertTrue(result, msg="raised error when option in param_options")        


        params = ["blom", "blom2", "blom3"]
        result = param_options("blom", params, "param_name", "func_name")
        self.assertTrue(result, msg="raised error when option in param_options")


if __name__ == "__main__":
    unittest.main()    
