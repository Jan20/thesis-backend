import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database
from tests.set_up import set_up
from tests.samples import Samples
from models.session import Session

class Test_Session(unittest.TestCase):

    #
    # Calculates the average performance for
    # every user stored at Firebase.
    #
    def test_from_dict(self):

        set_up()

        database: Database = Database()

        result: Session = database.get_session(Samples.sample_user.user_key, Samples.sample_session.session_key)

        timestamp = result.to_dict()['timestamp']
        
        expected_result: Session = Samples.sample_session
        expected_result.timestamp = timestamp

        #
        #
        #
        self.assertEqual(result.to_dict(), expected_result.to_dict())

if __name__ == '__main__':
    
    unittest.main(exit=False)