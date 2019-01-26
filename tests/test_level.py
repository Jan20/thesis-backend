import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database
from normalization.normalization import Normalization
from tests.set_up import set_up
from tests.set_up import clean_up
from tests.samples import Samples

class Test_Level(unittest.TestCase):

    set_up()

    result = Samples

if __name__ == '__main__':
    
    unittest.main(exit=False)