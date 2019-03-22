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
from tests.set_up import set_up_two_sample_users

class Test_Evolution(unittest.TestCase):

    def test_setup(self):

        clean_up()
        self.assertEqual(True, True)


    def test_execute(self):

        set_up_training_data()

        result: str = Evolution().execute('user_001')

        
        # Assuming that the hightest session stored for
        # the sample user should be 'session_042'.
        
        self.assertEqual(result, 'session_004')

        clean_up()

    
    def test_execute2(self):

        set_up_two_sample_users()

        result: str = Evolution().execute('user_002')   

        
        # Assuming that the hightest session stored for
        # the sample user should be 'session_042'.
        
        self.assertEqual(result, 'session_003')

        clean_up()



    def test_select_column(self):
        
        np.random.seed(2)

        random_distribution: [float] = np.random.rand(5)

        position, random_distribution = Evolution().select_column(random_distribution)
    
        self.assertEqual(position, 2)

        clean_up()

    def test_select_row(self):
       
        evolution: Evolution = Evolution()

        # Test 1

        row : [str] = ['.', '.', '.', '.', '.', 'X', '.', '.', 'X', '.', '.', 'X', '.', 'X']

        result: int = evolution.select_row(row, 'F')
        
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

        # Test 3

        column : [str] = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'X', 'X', 'X', 'X']

        result: int = evolution.compute_potential_positions_for_opponent_type_1(column)
        
        expected_result: [int] = [9]

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