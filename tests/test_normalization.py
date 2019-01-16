import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database
from normalization.normalization import Normalization
from tests.set_up import set_up
from tests.set_up import clean_up

class Test_Normalization(unittest.TestCase):

    #
    # Calculates the average performance for
    # every user stored at Firebase.
    #
    def test_calculate_average_performance(self):

        set_up()

        #
        # 
        #
        result: dict = Normalization().calculate_average_performance('user_042').to_dict()

        #
        # Expected Result
        #
        expected_result: dict = {
            
            'defeated_by_gaps': 1.0, 
            'defeated_by_opponent_type_1': 1.0, 
            'defeated_by_opponent_type_2': 1.0, 
            'defeated_by_opponent_type_3': 0.0

        }

        #
        #
        #
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    
    unittest.main(exit=False)