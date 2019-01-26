import os
import sys
import unittest
import random
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.level import Level
from evolution.evolution import Evolution
from database.database import Database
from tests.samples import Samples
from tests.set_up import set_up
from tests.set_up import clean_up

class Test_Evolution(unittest.TestCase):

    def test_execute(self):

        set_up()

        result: str = Evolution().execute(Samples.sample_user.user_key)

        #
        # Assuming that the hightest session stored for
        # the sample user should be 'session_042'.
        #
        self.assertEqual(result, 'session_043')

        clean_up()

    def test_evolve(self):

        set_up()

        result: Level = Evolution().evolve(Samples.sample_level)

        sample_level: Level =Samples.sample_level
        sample_level.representation[1][2] = 'C'
        sample_level.representation[1][3] = 'C'
        sample_level.representation[1][4] = 'C'
        sample_level.representation[1][5] = 'C'
        sample_level.representation[1][6] = 'C'
        sample_level.representation[1][7] = 'C'


        expected_result: Level = sample_level
    
        self.assertEqual(result, expected_result)

        clean_up()

    def test_select_column(self):
        
        np.random.seed(2)

        random_distribution: [float] = np.random.rand(5)

        position, random_distribution = Evolution().select_column(random_distribution)
    
        self.assertAlmostEquals(position, 2)

        clean_up()

    def test_select_row(self):

        sample_level: Level = Samples.sample_level

        columns = np.array(sample_level.representation)
        
        result: int = Evolution().select_row(columns[:, 0])

        expected_result = 13

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    
    unittest.main(exit=False)