"""Tests if  ``is_empty`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/data_frames/test_is_empty.py
    or
    python -m unittest -b tests/data_frames/test_is_empty.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import pandas as pd


### FUNCTION IMPORT ###
from paramcheckup.data_frames import is_empty


os.system('cls')



class Test_is_empty(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.df = pd.DataFrame({
            "Column A": [1, 2, 4, 5, ]
        })

    def test_outputs(self):
        output = is_empty(self.df, "parametro", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        output = is_empty(data_frame=self.df, param_name="parametro", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")        

    def test_is_missing_input(self):
        with self.assertRaises(ValueError, msg="Does not raised error when the dataframe is empty"):
            df = pd.DataFrame({})
            is_empty(df, param_name="df", func_name="func_name")




if __name__ == "__main__":
    unittest.main()    