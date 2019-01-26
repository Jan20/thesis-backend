import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database
from models.performance import Performance
from tests.samples import Samples


class Test_Performance(unittest.TestCase):

    #
    # Calculates the average performance for
    # every user stored at Firebase.
    #
    def test_from_dict(self):


        # Should create a new Performance object
        result: Performance = Performance.from_dict(Samples.sample_performance_dict)

        # Expected Result
        expected_result: Performance = Samples.sample_performance

        #
        self.assertEqual(result.to_dict(), expected_result.to_dict())


if __name__ == '__main__':
    
    unittest.main(exit=False)