"""Tests if  ``is_list_of_types`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/types/test_is_list_of_types.py
    or
    python -m unittest -b tests/types/test_is_list_of_types.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest


### FUNCTION IMPORT ###
from paramcheckup.types import is_list_of_types


os.system('cls')



class Test_is_list_of_types(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.my_list = [1, 2, 3, 4]
        cls.expected_type = int

    def test_outputs(self):
        output = is_list_of_types(self.my_list, "param_name", "func_name", self.expected_type)
        self.assertTrue(output, msg="not True when must be True")
        output = is_list_of_types(my_list=self.my_list, param_name="param_name", func_name="func_name", expected_type=self.expected_type)
        self.assertTrue(output, msg="not True when must be True")   

    def test_pass_ints(self):
        my_list = [1, 2, 3, 4]
        my_type = int
        self.assertTrue(is_list_of_types(my_list, "param_name", "func_name", my_type), msg="not True when list of ints")


    def test_pass_floats(self):
        my_list = [1.1, 2.2, 3.3, 4.4]
        my_type = float
        self.assertTrue(is_list_of_types(my_list, "param_name", "func_name", my_type), msg="not True when list of floats")

    def test_pass_str(self):
        my_list = ["Anderson", "Marcos", "Dias"]
        my_type = str
        self.assertTrue(is_list_of_types(my_list, "param_name", "func_name", my_type), msg="not True when list of str")        

    def test_pass_lists(self):
        my_list = [["Anderson"], ["Marcos"], ["Dias"]]
        my_type = list
        self.assertTrue(is_list_of_types(my_list, "param_name", "func_name", my_type), msg="not True when list of lists")                

    def test_pass_dicts(self):
        my_list = [{"Anderson": 1}, {"Marcos": 2}, {"Dias": 4}]
        my_type = dict
        self.assertTrue(is_list_of_types(my_list, "param_name", "func_name", my_type), msg="not True when list of lists")                




    def test_string(self):
        with self.assertRaises(TypeError, msg="Does not raised error when has a str when it should not"):
            my_list = ["1", "2", 3]
            my_type = str
            is_list_of_types(my_list, "param_name", "func_name", my_type)

    def test_int(self):
        with self.assertRaises(TypeError, msg="Does not raised error when has a int when it should not"):
            my_list = ["1", "2", 3]
            my_type = int
            is_list_of_types(my_list, "param_name", "func_name", my_type)            

    def test_float(self):
        with self.assertRaises(TypeError, msg="Does not raised error when has a float when it should not"):
            my_list = ["1", "2", 3.1]
            my_type = float
            is_list_of_types(my_list, "param_name", "func_name", my_type)   

    def test_mixed_types(self):
        with self.assertRaises(TypeError, msg="Does not raised error when has a mixed_types when it should not"):
            my_list = ["1", {"2": 2}, 3.1, 2, [1,2], (1,2,3)]
            my_type = float
            is_list_of_types(my_list, "param_name", "func_name", my_type)                                    



if __name__ == "__main__":
    unittest.main()    