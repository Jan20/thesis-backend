import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.level import Level
from evolution.evolution import Evolution
from database.database import Database
from tests.samples import Samples
from tests.set_up import set_up
from tests.set_up import clean_up

class Test_Evolution(unittest.TestCase):



    def test_evolve(self):

        set_up()

        Evolution(Samples.sample_user.user_key, Samples.sample_session.session_key, Samples.sample_level.key).execute()


        clean_up()
        # self.assertEqual(result, expected_result)


if __name__ == '__main__':
    
    unittest.main(exit=False)