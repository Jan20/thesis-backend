import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.level import Level
from evolution.evolution import Evolution
from database.database import Database
from tests.samples import Samples

class Test_Evolution(unittest.TestCase):

    def set_up(self):

        database: Database = Database()

        database.store_user(Samples.sample_user)
        database.store_session(Samples.sample_user.user_key, Samples.sample_session)
        database.store_level(Samples.sample_user.user_key, Samples.sample_session.session_key, Samples.sample_level)

    def clean_up(self):

        Database().delete_user(Samples.sample_user)


    def test_evolve(self):

        self.set_up()

        Evolution(Samples.sample_user.user_key, Samples.sample_session.session_key, Samples.sample_level.key).execute()

            
        self.clean_up()
        # self.assertEqual(result, expected_result)


if __name__ == '__main__':
    
    unittest.main(exit=False)