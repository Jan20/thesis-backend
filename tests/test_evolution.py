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
from tests.set_up import set_up_training_data

class Test_Evolution(unittest.TestCase):

    # def test_execute(self):

        # set_up_training_data()

        # result: str = Evolution().execute('user_001')

        #
        # Assuming that the hightest session stored for
        # the sample user should be 'session_042'.
        #
        # self.assertEqual(result, 'session_043')

        # clean_up()

    # def test_evolve(self):

    #     set_up()

    #     result: Level = Evolution().evolve(Samples.sample_level)

    #     sample_level: Level =Samples.sample_level
    #     sample_level.representation[1][2] = 'C'
    #     sample_level.representation[1][3] = 'C'
    #     sample_level.representation[1][4] = 'C'
    #     sample_level.representation[1][5] = 'C'
    #     sample_level.representation[1][6] = 'C'
    #     sample_level.representation[1][7] = 'C'


    #     expected_result: Level = sample_level
    
    #     self.assertEqual(result, expected_result)

    #     clean_up()

    # def test_select_column(self):
        
    #     np.random.seed(2)

    #     random_distribution: [float] = np.random.rand(5)

    #     position, random_distribution = Evolution().select_column(random_distribution)
    
    #     self.assertAlmostEquals(position, 2)

    #     clean_up()

    def test_select_row(self):
       
        evolution: Evolution = Evolution()

        # Test 1

        row : [str] = ['.', '.', '.', '.', '.', 'X', '.', '.', 'X', '.', '.', 'X', '.', 'X']

        result: int = evolution.select_row(row, 'V')
        
        expected_result: int = 0

        self.assertEqual(result, expected_result)

        # Test 2

        row : [str] = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'X']

        result: int = evolution.select_row(row, 'C')
        
        expected_result: int = 12

        self.assertEqual(result, expected_result)

        # Test 3

        row : [str] = ['X', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']

        result: int = evolution.select_row(row, 'C')
        
        expected_result: int = 404

        self.assertEqual(result, expected_result)

        # Test 4

        row : [str] = ['.', 'X', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']

        result: int = evolution.select_row(row, 'C')
        
        expected_result: int = 0

        self.assertEqual(result, expected_result)


    def test_compute_potential_positions_for_opponent_type_1(self):

        evolution: Evolution = Evolution()

        # Test 1

        column: [str] = ['.', '.', 'X', '.', '.', 'X', '.', '.', 'X', '.', '.', 'X', '.', 'X']

        result: int = evolution.compute_potential_positions_for_opponent_type_1(column)

        expected_result = [1, 4, 7, 10, 12]

        self.assertEqual(result, expected_result)

        # Test 2

        column : [str] = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'X']

        result: int = evolution.compute_potential_positions_for_opponent_type_1(column)
        
        expected_result: [int] = [12]

        self.assertEqual(result, expected_result)
    
    #
    #
    #    
    def test_compute_potential_positions_for_opponent_type_2(self):

        evolution: Evolution = Evolution()

        # Test 1

        column: [str] = ['.', '.', 'X', '.', '.', 'X', '.', '.', 'X', '.', '.', 'X', '.', 'X']

        result: int = evolution.compute_potential_positions_for_opponent_type_1(column)

        expected_result = [1, 4, 7, 10, 12]

        self.assertEqual(result, expected_result)

        # Test 2

        column : [str] = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'X']

        result: int = evolution.compute_potential_positions_for_opponent_type_1(column)
        
        expected_result: [int] = [12]

        self.assertEqual(result, expected_result)

    #
    #
    #
    def test_compute_potential_positions_for_opponent_type_3(self):

        evolution: Evolution = Evolution()

        # Test 1

        column: [str] = ['.', '.', 'X', '.', '.', 'X', '.', '.', 'X', '.', '.', 'X', '.', 'X']

        result: int = evolution.compute_potential_positions_for_opponent_type_3(column)

        expected_result = []

        self.assertEqual(result, expected_result)

        # Test 2

        column: [str] = ['.', '.', '.', '.', '.', 'X', '.', '.', 'X', '.', '.', 'X', '.', 'X']

        result: int = evolution.compute_potential_positions_for_opponent_type_3(column)

        expected_result = [0]

        self.assertEqual(result, expected_result)

        # Test 3

        column: [str] = ['.', '.', '.', '.', '.', '.', '.', '.', 'X', '.', '.', 'X', '.', 'X']

        result: int = evolution.compute_potential_positions_for_opponent_type_3(column)

        expected_result = [0, 1, 2, 3]

        self.assertEqual(result, expected_result)

        # Test 4

        column: [str] = ['.', 'X', '.', 'X', '.', 'X', 'X', '.', '.', '.', '.', '.', '.', '.']

        result: int = evolution.compute_potential_positions_for_opponent_type_3(column)

        expected_result = [7]

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    
    unittest.main(exit=False)