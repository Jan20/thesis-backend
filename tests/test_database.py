import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from computations.transform import Transform
from database.database import Database
from models.user import User
from models.level import Level
from models.performance import Performance
from models.session import Session

from tests.samples import Samples

class Test_Database(unittest.TestCase):
    Database().delete_users()

    def test_store_user(self):

        database: Database = Database()

        database.store_user(Samples.sample_user)

        user: User = database.get_user(Samples.sample_user.user_key)

        self.assertEqual(user.to_dict(), Samples.sample_user.to_dict())
    
    #
    # Calculates the average performance for
    # every user stored at Firebase.
    #
    def test_get_user_keys(self):

        database: Database = Database()
        
        database.store_user(Samples.sample_user)

        #
        #
        #
        result: [str] = database.get_user_keys()

        #
        #
        #
        expected_result: [str] = ['user_042']

        #
        #
        #
        self.assertEqual(result, expected_result)
    
    def test_get_generic_level(self):

        #
        #
        #
        result: dict() = Database().get_generic_level('level_01').to_dict()
        
        #
        #
        #
        self.assertEqual(result, Samples.sample_level)


    def test_store_level(self):

        database: Database = Database()
        database.store_user(Samples.sample_user)
        database.store_session('user_042', Samples.sample_session)
        
        database.store_level('user_042', 'session_042', Samples.sample_level)

        level: Level = database.get_level('user_042', 'session_042', Samples.sample_level.key)

        self.assertEqual(level.to_dict(), Samples.sample_level.to_dict())

        

if __name__ == '__main__':
    
    unittest.main(exit=False)