import time
import unittest
import sys
sys.path.append("../..")
from utilities.utils import *

class TestUtils(unittest.TestCase):

    def test_find_string_in_other_string(self):

        name = find_string_in_other_string("mars selfies",["mars screenshot","marsselfies","mars"])
        self.assertEqual(name,"marsselfies")

if __name__ == '__main__':
    unittest.main()
