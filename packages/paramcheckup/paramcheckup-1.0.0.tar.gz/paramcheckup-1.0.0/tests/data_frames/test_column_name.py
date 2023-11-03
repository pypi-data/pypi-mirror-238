"""Tests if  ``column_name`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/data_frames/test_column_name.py
    or
    python -m unittest -b tests/data_frames/test_column_name.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import pandas as pd


### FUNCTION IMPORT ###
from paramcheckup.data_frames import column_name


os.system('cls')



class Test_column_name(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.data_frame = pd.DataFrame({
            "A": [1,2,3],
            "B": [4,5,6],
        })
        cls.name_a = "A"
        cls.name_b = "B"

    def test_outputs(self):
        output = column_name("A", self.data_frame, "param_name", "func_name")
        self.assertTrue(output, msg="not True when must be True")
        output = column_name("B", self.data_frame, "param_name", "func_name")
        self.assertTrue(output, msg="not True when must be True")        
        output = column_name(column_name="B", data_frame=self.data_frame, param_name="param_name", func_name="func_name")
        self.assertTrue(output, msg="not True when must be True")                



    def test_raises(self):
        with self.assertRaises(ValueError, msg="Does not raised ValueError when value column_name not in dataframe"):
            column_name("C", self.data_frame, "param_name", "func_name")
        with self.assertRaises(ValueError, msg="Does not raised ValueError when value column_name not in dataframe"):
            column_name(1, self.data_frame, "param_name", "func_name")            




if __name__ == "__main__":
    unittest.main()    