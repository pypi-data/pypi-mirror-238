"""Tests if the new version is set to be higher than the current version

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/versioning/test_new_version.py
    or
    python -m unittest -b tests/versioning/test_new_version.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import toml


### FUNCTION IMPORT ###
from packaging import version


os.system("cls")


class Test_version(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current_version = "1.0.0"
        cls.next_version = "1.0.1"  # need to be change

    def test_current_version(self):
        pyproject_version = toml.load("pyproject.toml")["project"]["version"]
        self.assertTrue(
            version.parse(pyproject_version) == version.parse(self.current_version),
            msg="versions doesn't match",
        )

    def test_next_version(self):
        pyproject_version = toml.load("pyproject.toml")["project"]["version"]
        self.assertTrue(
            version.parse(pyproject_version) < version.parse(self.next_version),
            msg="current version greater or equal than future version",
        )


if __name__ == "__main__":
    unittest.main()
