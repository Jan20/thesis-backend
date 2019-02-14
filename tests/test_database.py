import os, sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database
from models.user import User
from models.level import Level
from models.performance import Performance
from models.session import Session

from tests.samples import Samples
from tests.set_up import set_up
from tests.set_up import clean_up

class Test_Database(unittest.TestCase):

    #######################
    # User Related Tests ##
    #######################
    Database().delete_users()

    def test_store_user(self):

        database: Database = Database()

        database.store_user(Samples.sample_user)

        user: User = database.get_user(Samples.sample_user.user_key)

        self.assertEqual(user.to_dict(), Samples.sample_user.to_dict())

    def test_delete_users(self):

        database: Database = Database()

        database.store_user(Samples.sample_user)

        database.delete_users()

        result = database.get_user_keys()

        expected_result: [str] = []

        self.assertEqual(result, expected_result)
    
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

    ###########################
    ## Session Related Tests ##
    ###########################
    def test_get_session(self):

        set_up()

        # Should retrieve an existing session from Firestore.
        result: Session = Database().get_session(Samples.sample_user.user_key, Samples.sample_session.session_key)
        timestamp = result.to_dict()['timestamp']

        # Defines the expected result.            
        expected_result: Session = Samples.sample_session
        expected_result.timestamp = timestamp
        
        # Expects the result to be equal to a predefined sample session.
        self.assertEqual(result.to_dict(), expected_result.to_dict())

        clean_up()

    def test_store_level(self):

        database: Database = Database()
        database.store_user(Samples.sample_user)
        database.store_session('user_042', Samples.sample_session)
        
        database.store_level('user_042', 'session_042', Samples.sample_level)

        level: Level = database.get_level('user_042', 'session_042', Samples.sample_level.key)

        self.assertEqual(level.to_dict(), Samples.sample_level.to_dict())

        clean_up()

    def test_set_average_performance(self):

        database: Database = Database()
        database.store_user(Samples.sample_user)
        database.store_session(Samples.sample_user.user_key, Samples.sample_session)

        database.set_average_performance('user_042', Samples.sample_performance)

        result: Performance = database.get_average_performance('user_042')
        expected_result: Performance = Samples.sample_performance

        self.assertEqual(result.to_dict(), Samples.sample_performance.to_dict())

        clean_up()

    def test_get_session_ids(self):

        database: Database = Database()
        database.store_user(Samples.sample_user)
        database.store_session(Samples.sample_user.user_key, Samples.sample_session)

        result: [int] = database.get_session_ids(Samples.sample_user.user_key)

        self.assertEqual(result, [42])

        clean_up()


    def test_get_performance(self):

        database: Database = Database()
        database.store_user(Samples.sample_user)
        database.store_session(Samples.sample_user.user_key, Samples.sample_session)

        result: Performance = database.get_performance(Samples.sample_user.user_key, Samples.sample_session.session_key)

        expected_result: Performance = Samples.sample_session.performance

        self.assertEqual(result.to_dict(), expected_result.to_dict())

        clean_up()

    def test_get_session_keys(self):

        database: Database = Database()
        database.store_user(Samples.sample_user)
        database.store_session(Samples.sample_user.user_key, Samples.sample_session)        
        
        result = database.get_session_keys('user_042')

        expected_result: [str] = ['session_042']

        self.assertEqual(result, expected_result)

        clean_up()


if __name__ == "__main__":

    unittest.main(exit=False)

