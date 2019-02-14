import os
import sys
import random
import string
import random
import numpy as np

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
        random_level: Level = database.get_random_level()

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

            random_number: float = random.randint(0, 2)
            
            opponent_type: str

            if random_number == 0:
                
                opponent_type = 'C'
            
            if random_number == 1:
                
                opponent_type = 'J'

            if random_number == 2:
                
                opponent_type = 'V'

            # Selects a column
            column, random_distribution = self.select_column(random_distribution)

            #
            row: int = self.select_row(matrix[:, column], opponent_type)

           

            #
            if row == 404: 

                continue
            
        
            level.representation[row][column] = opponent_type

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
    def select_row(self, column: [str], opponent_type: str) -> int:

        # String array which 
        potential_positions: [int]

        # 
        position_of_tile: int = 404

        if opponent_type == 'C':

            potential_positions = self.compute_potential_positions_for_opponent_type_1(column)

        if opponent_type == 'J':

            potential_positions = self.compute_potential_positions_for_opponent_type_2(column)

        if opponent_type == 'V':

            potential_positions = self.compute_potential_positions_for_opponent_type_3(column)


        #
        #
        if len(potential_positions) > 0:

            index: int = random.randint(0, len(potential_positions)-1)

            position_of_tile = potential_positions[index]

        return position_of_tile

    #
    #
    #
    def compute_potential_positions_for_opponent_type_1(self, column: [str]) -> [int]:

        #
        potential_positions: [int] = []

        # Iterates over all tiles in a column
        for position, tile in enumerate(column):

            # Checks wether the 
            if tile == 'X' or tile == 'D' or tile == 'B':
                
                if (position > 0): 
                    
                    potential_positions.append(position - 1)

        return potential_positions

    #
    #
    #
    def compute_potential_positions_for_opponent_type_2(self, column: [str]) -> [int]:

        potential_positions: [int] = []

        # Iterates over all tiles in a column
        for position, tile in enumerate(column):

            # Checks wether the 
            if tile == 'X' or tile == 'D' or tile == 'B':
                
                potential_positions.append(position - 1)

        return potential_positions


    #
    #
    #
    def compute_potential_positions_for_opponent_type_3(self, column: [str]) -> [int]:

        potential_positions: [int] = []
        isPotentialSpot: bool
        
        # Iterates over all tiles in a column
        for position, _ in enumerate(column):

            isPotentialSpot = True

            for i in range(5):

                if ((position + i) < (len(column) - 2)):

                    if column[position + i] != '.':

                        isPotentialSpot = False

                else:

                    isPotentialSpot = False
            
            if isPotentialSpot:
                
                potential_positions.append(position)

        return potential_positions
