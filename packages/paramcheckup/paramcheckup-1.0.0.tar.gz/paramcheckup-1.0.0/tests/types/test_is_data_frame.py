"""Tests if  ``is_data_frame`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/types/test_is_data_frame.py
    or
    python -m unittest -b tests/types/test_is_data_frame.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import pandas as pd


### FUNCTION IMPORT ###
from paramcheckup.types import is_data_frame


os.system('cls')



class Test_is_data_frame(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.df = pd.DataFrame({
            "Column A": [1, 2, 4, 5, ]
        })

    def test_outputs(self):
        output = is_data_frame(self.df, "parametro", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        output = is_data_frame(data_frame=self.df, param_name="parametro", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")        

   
   

    def test_is_not_dataframe(self):
        with self.assertRaises(TypeError, msg="Does not raised error when type(df) != df.DataFrame"):
            is_data_frame(1, param_name="df", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when type(df) != df.DataFrame"):
            is_data_frame("!", param_name="df", func_name="func_name")
        with self.assertRaises(TypeError, msg="Does not raised error when type(df) != df.DataFrame"):
            is_data_frame([1], param_name="df", func_name="func_name")


    def test_pass(self):
        df = pd.DataFrame(columns=["a", 'b'])
        df["a"] = [1, 2]
        df["b"] = [3, 4]
        result = is_data_frame(df, param_name="df", func_name="func_name")
        self.assertTrue(result, msg = "Returning False when the input is a DataFrame")


    # def test_is_missing_input(self):
    #     # with self.assertRaises(TypeError, msg="Does not raised error when the dataframe is empty"):
    #     df = pd.DataFrame({})
    #     print(type(df))
    #     print("ok")
    #     print(df.empty)
    #     is_data_frame(df, param_name="df", func_name="func_name")




if __name__ == "__main__":
    unittest.main()    