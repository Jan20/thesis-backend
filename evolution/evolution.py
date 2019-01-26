import os
import sys
import random
import string
import random
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database
from models.level import Level
from models.user import User
from database.database import Database
from models.level import Level
from normalization.normalization import Normalization

#
#
#
class Evolution(object):
    
    ###############
    ## Functions ##
    ###############

    #
    # Wraps up the generation of a new session for a
    # given user.
    #
    def execute(self, user_key: str) -> str:

        # Creates a new database object.
        database: Database = Database()

        # Selects a new level randomly.
        random_level: Level = database.get_random_level('')

        # Difficulty score that should be reached.
        difficulty: float = Normalization().calculate_user_score(user_key)

        # evolves the previously selected level.
        evolved_level: Level = self.evolve(difficulty, random_level)

        # Generates a new session and connects the evolved
        # level to that session.
        session_key: str = database.generate_session(user_key, evolved_level, difficulty)
    
        # Returns the key of the previously generated session.
        return session_key

    #
    #
    #
    def evolve(self, target_score: int, level: Level) -> Level:

        # Creates an array storing a random distribution of values
        # corresponding to the level's length. 
        random_distribution: [float] = np.random.rand(len(level.representation[0]))

        # Converts the two-dimentional level representation into
        # a two-dimentional numpy array.
        matrix = np.array(level.representation)

        # Goes as long as the level's desired difficulty is not reached.
        while target_score > 0:

            # Selects a column
            column, random_distribution = self.select_column(random_distribution)

            row: int = self.select_row(matrix[:, column])

            if row == 404: 

                continue

            level.representation[row][column] = 'C'

            target_score -= 5

        return level

    #
    # Selects a column based on the highest value from an array
    # filled with a selection of randomely chosen values.
    #
    def select_column(self, random_distribution: [float]) -> (int, [float]):

        # Stores the position of the highest random value
        # within the random distribution array. 
        position_of_highest_value: int = 0

        # Stores the highest value within the random distribution.
        highest_value: float = random_distribution[0]
        
        # Iterate over all elements within the random distribution.
        for position, value in enumerate(random_distribution):

            # Checks whether the current value is higher than
            # the previously stored one.
            if value > highest_value:

                # Writes the value of the former highest value to
                # its former position since it has been replaced by
                # zero in order to ensure that every value is only
                # picked once.
                random_distribution[position_of_highest_value] = highest_value
                
                # The current position is stored as the new position
                # of the highest value.
                position_of_highest_value: int = position

                # The current value is stored as the new highest value.
                highest_value: float = value

                # Writes the value corresponding to the current position
                # is set to be zero in order to ensure that every value
                # gets only picked once.
                random_distribution[position] = 0

        # Returns the highest value within the array of random values, as 
        # well as an updated version of the random distribution.
        return position_of_highest_value, random_distribution

    #
    #
    #
    def select_row(self, column: [str]) -> int:

        potential_spots: [str] = []

        # 
        position_of_tile: int = 404

        #
        for position, tile in enumerate(column):

            if tile == 'X' or tile == 'D' or tile == 'B':
                
                if (position_of_tile == 404):
                    
                    position_of_tile = position - 1

        return position_of_tile

