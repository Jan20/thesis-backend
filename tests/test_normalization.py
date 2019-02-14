import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database
from normalization.normalization import Normalization
from tests.set_up import set_up
from tests.set_up import clean_up
from tests.set_up import set_up_training_data
from tests.samples import Samples

class Test_Normalization(unittest.TestCase):

    
    # Calculates the average performance for
    # every user stored at Firebase.
    def test_calculate_user_score(self):

        # Sets up a test environment.
        set_up()

        # Calculates the user score for a sample user.
        result: int = Normalization().calculate_user_score(Samples.sample_user.user_key)

        # Expects the user score to be 100.
        expected_result: int = 100

        # Assets whether the result is equals the expected result.
        self.assertEqual(result, expected_result)

        # Removes the test environment.
        clean_up()


    def test_normalize_performance(self):

        # Sets up a test environment.
        set_up()

        #
        df = Normalization().normalize_performance()

        result = df.loc[['user_042']].values

        excepted_result = [[  1.,   1.,   1.,   0., 1.,  1.,  1., 1.]]

        self.assertEqual(result[0][0], excepted_result[0][0])
        self.assertEqual(result[0][1], excepted_result[0][1])
        self.assertEqual(result[0][2], excepted_result[0][2])
        self.assertEqual(result[0][3], excepted_result[0][3])
        self.assertEqual(result[0][4], excepted_result[0][4])
        self.assertEqual(result[0][5], excepted_result[0][5])
        self.assertEqual(result[0][6], excepted_result[0][6])
        self.assertEqual(result[0][7], excepted_result[0][7])

        clean_up()


    def test_calculate_average_performance(self):

        set_up()

        df = Normalization().calculate_average_performance('user_042')

        result = df.loc[['user_042']].values

        excepted_result = [[  1.,   1.,   1.,   0., 600.,  45.,  15., 80]]

        self.assertEqual(result[0][0], excepted_result[0][0])
        self.assertEqual(result[0][1], excepted_result[0][1])
        self.assertEqual(result[0][2], excepted_result[0][2])
        self.assertEqual(result[0][3], excepted_result[0][3])
        self.assertEqual(result[0][4], excepted_result[0][4])
        self.assertEqual(result[0][5], excepted_result[0][5])
        self.assertEqual(result[0][6], excepted_result[0][6])
        self.assertEqual(result[0][7], excepted_result[0][7])

        clean_up()

    def test_create_DataFrame(self):

        set_up()

        df = Normalization().create_DataFrame('user_042')

        result = df.loc[['user_042:session_042']].values

        excepted_result = [[  1.,   1.,   1.,   0., 600.,  45.,  15., 80]]

        self.assertEqual(result[0][0], excepted_result[0][0])
        self.assertEqual(result[0][1], excepted_result[0][1])
        self.assertEqual(result[0][2], excepted_result[0][2])
        self.assertEqual(result[0][3], excepted_result[0][3])
        self.assertEqual(result[0][4], excepted_result[0][4])
        self.assertEqual(result[0][5], excepted_result[0][5])
        self.assertEqual(result[0][6], excepted_result[0][6])
        self.assertEqual(result[0][7], excepted_result[0][7])

        clean_up()

if __name__ == '__main__':
    
    unittest.main(exit=False)