import os
import sys
import random
import numpy as np
import pandas as pd

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
        random_level: Level = database.get_random_level()

        target_score: int = 100

        # Difficulty score that should be reached.
        difficulty_class: str = Normalization().calculate_quantiles(user_key)
        print(difficulty_class)

        if difficulty_class == 'class_01': target_score = 50
        if difficulty_class == 'class_02': target_score = 75
        if difficulty_class == 'class_03': target_score = 100
        if difficulty_class == 'class_04': target_score = 125
        if difficulty_class == 'class_05': target_score = 150

        if difficulty_class == 'random_distribution': target_score = 100

        # evolves the previously selected level.
        evolved_level: Level = self.evolve(difficulty_class, random_level)

        # Generates a new session and connects the evolved
        # level to that session.
        session_key: str = database.generate_session(user_key, evolved_level, target_score)
    
        # Returns the key of the previously generated session.
        return session_key

    #
    # 
    #
    def evolve(self, difficulty_class: str, level: Level) -> Level:

        if (difficulty_class == 'random_distribution'):

            level = self.place_opponents_randomly(16, level)

        if (difficulty_class == 'class_01'):
        
            level = self.place_opponents_randomly(24, level)
            level = self.place_opponents_next_to_each_other(1, level)
            level = self.place_opponents_close_to_choke_points(1, level)
        
        if (difficulty_class == 'class_02'):
    
            level = self.place_opponents_randomly(12, level)
            level = self.place_opponents_next_to_each_other(6, level)
            level = self.place_opponents_close_to_choke_points(4, level)

        if (difficulty_class == 'class_03'):
        
            level = self.place_opponents_randomly(5, level)
            level = self.place_opponents_next_to_each_other(9, level)
            level = self.place_opponents_close_to_choke_points(8, level)


        if (difficulty_class == 'class_04'):
        
            level = self.place_opponents_randomly(3, level)
            level = self.place_opponents_next_to_each_other(11, level)
            level = self.place_opponents_close_to_choke_points(14, level)

        if (difficulty_class == 'class_05'):
        
            level = self.place_opponents_randomly(1, level)
            level = self.place_opponents_next_to_each_other(12, level)
            level = self.place_opponents_close_to_choke_points(24, level)

        return level


    #
    # Populates a given level with a number of opponents
    # defined by the amount parameter.
    #
    def place_opponents_randomly(self, amount: int, level: Level) -> Level:

        # Defines an empty dataframe intended to store a range of
        # opponents with their type and their position within the given level.
        df = pd.DataFrame(columns=['row', 'column', 'opponent_type']).astype(int)

        # Tries to find new potential positions as long as the
        # specified amount of opponents is not reached yet.
        while len(df) < amount:

            # Selects a walking, jumping or flying opponent randomly.
            opponent_type: str = random.choice(['C', 'J', 'F'])
            
            # Calculates a random position for an opponent belonging
            # to the type that have been defined above. 
            random_positions = self.position_opponent_randomly(np.array(level.representation), opponent_type)
            
            # Iterates over the random_positions dataframe which may 
            # either contain a single valid position or in case that no 
            # position could have been found, it should be empty. 
            for _, entry in random_positions.iterrows(): 

                # The opponent defined above is added to the current level
                level.representation[entry['row']][entry['column']] = entry['opponent_type']            
            
            # Adds the randomly chosen opponent to the dataframe
            # defined above in order to ensure that the while loop
            # terminates eventually.
            df = df.append(random_positions)

        # Returns the level that has been passed to the function as parameter
        # and has been extended by a range of randomly selected opponents.
        return level
        
    #
    # Position an opponent of a given type in a random fashion.
    #
    def position_opponent_randomly(self, level: [[str]], opponent_type: str) -> pd.core.frame.DataFrame:
        
        # Creates an empty dataframe intended to store an
        # opponent's position in terms of an x and y coordinate
        # denoted with 'row' and 'column' as well as the opponent's type.
        df = pd.DataFrame(columns=['row', 'column', 'opponent_type']).astype(int)

        # Chooses a column in a random fashion. The first 
        column: int = np.random.randint(7, len(level[0]) - 1)

        # String array intended to store potential 
        # positions to place an opponent.
        potential_positions: [int] = []

        # Iterates over all rows in a column.
        for row, _ in enumerate(level[:, column]):

            # Checks whether the current location
            # can be regared as to be valid.
            is_valid: bool = self.check_for_candidate(row, column, level, opponent_type)
            
            # If all previously defined conditions are met,
            # the current row is added to the potential_positions
            # array.
            if is_valid and opponent_type == 'F': potential_positions.append(row - 5)
            if is_valid and opponent_type != 'F': potential_positions.append(row - 1)
        
        # Checks wether at least one potential position has been identified.
        if len(potential_positions) > 0:    

            # Selects a random location from the array of potential positions.
            data = [random.choice(potential_positions), column, opponent_type]
            
            # Adds the selected position to the dataframe defined above.
            df = df.append(pd.DataFrame([data], columns=['row', 'column', 'opponent_type'], index=[f'col:{column}']))
        
        # Returns the dataframe defined above which can either be
        # empty or exibit exactly one entry.
        return df 

    #
    #
    #
    def place_opponents_next_to_each_other(self, amount: int, level: Level) -> Level:

        # Dataframe intended to store randomly a range of opponents
        # that are randomly assigned to a position.
        df = pd.DataFrame(columns=['row', 'column', 'opponent_type']).astype(int)

        # Goes as long as the level's desired amount of 
        # opponents has not been reached yet.
        while len(df) < amount:
            
            # Selects a walking, jumping or flying opponent randomly.
            opponent_type: str = random.choice(['J', 'F'])
            
            # Calculates a random position for an opponent belonging
            # to the type that have been defined above. 
            random_positions = self.position_opponents_next_to_each_other(np.array(level.representation), opponent_type)
            
            # Iterates over the random_positions dataframe which may 
            # either contain a single valid position or in case that no 
            # position could have been found, it should be empty. 
            for _, entry in random_positions.iterrows(): 
                
                # The opponent defined above is added to the current level
                level.representation[entry['row']][entry['column']] = entry['opponent_type']            
            
            # Adds the randomly chosen opponent to the dataframe
            # defined above in order to ensure that the while loop
            # terminates eventually.
            df = df.append(random_positions)
        
        return level
  
    #
    #
    #
    #
    def position_opponents_next_to_each_other(self, level: [[str]], opponent_type: str):
        
        df = pd.DataFrame(columns=['row', 'column', 'opponent_type']).astype(int)

        row: int
        column: int
        
        df = self.position_opponent_randomly(level, opponent_type)
        
        if df is not None:

            for _, entry in df.iterrows():

                if opponent_type == 'F': row = entry['row'] + 5
                if opponent_type != 'F': row = entry['row'] + 1
            
                column = entry['column'] + 1

                if not (

                    # Checks wether the tile over the current one
                    # is an empty one, which guarantees that the
                    # opponent can be reached by the player.
                    level[row - 1, column] == '.' and
                    
                    # Checks whether the current tile is a solid one
                    # in order to make sure that an opponent is not
                    # spawned in mid air.
                    self.check_tile(level[row, column]) and

                    # Checks whether the selected opponent type can
                    # be spawned at the current location.
                    self.check_position(row, column, level, opponent_type) and not 
                    
                    # Makes sure that the current tile is not already
                    # occupied by a previously placed opponent.
                    self.check_for_opponents(row, column, level)
               
                ): return df

                # If all previously defined conditions are met,
                # the current row is added to the potential_positions
                # array.
                if opponent_type == 'F': row = row - 5
                if opponent_type != 'F': row = row - 1
                    
                data = [row, column, opponent_type]
                
                df = df.append(pd.DataFrame([data], columns=['row', 'column', 'opponent_type'], index=[f'col:{column}']))
                
        return df

    #
    #
    #
    def place_opponents_close_to_choke_points(self, amount: int, level: Level) -> Level:

        # Dataframe intended to store randomly a range of opponents
        # that are randomly assigned to a position.
        df = pd.DataFrame(columns=['row', 'column', 'opponent_type']).astype(int)

        #
        choke_points = self.identify_choke_points(np.array(level.representation))

        # Goes as long as the level's desired amount of 
        # opponents has not been reached yet.
        while len(df) < amount or len(df) == len(choke_points):
            
            # Calculates a random position for an opponent belonging
            # to the type that have been defined above. 
            sample_choke_points = choke_points.sample(1)
            
            # Iterates over the random_positions dataframe which may 
            # either contain a single valid position or in case that no 
            # position could have been found, it should be empty. 
            for _, entry in sample_choke_points.iterrows(): 
                
                # The opponent defined above is added to the current level
                level.representation[entry['row']][entry['column']] = entry['opponent_type']            
            
            # Adds the randomly chosen opponent to the dataframe
            # defined above in order to ensure that the while loop
            # terminates eventually.
            df = df.append(sample_choke_points)

        return level


    #
    #
    #
    def identify_choke_points(self, level: [[str]]) -> pd.core.frame.DataFrame:
        
        df = pd.DataFrame(columns=['row', 'column', 'opponent_type']).astype(int)

        for col in range(len(level[0]) - 1):
            
            for row, tile in enumerate(level[:, col]):

                #
                opponent_type: str = random.choice(['J', 'F'])

                #

                is_choke = self.select_choke_point(row, col, tile, level, opponent_type)
               
                
                if opponent_type == 'F': row = row - 5
                if opponent_type != 'F': row = row - 1

                # Selects a walking, jumping or flying opponent randomly.
                data = [row, col, opponent_type]

                if is_choke: df = df.append(pd.DataFrame([data], columns=['row', 'column', 'opponent_type'], index=[f'{row}:{col}']))
        
        return df

    #
    # Checks whether the current coordinate comes into question to be
    # a valid choke point.
    #
    def select_choke_point(self, row: int, column: int, tile: str, level, opponent_type: str) -> bool:

        if not self.check_for_candidate(row, column, level, opponent_type): return False
        
        if self.check_for_bottom_row_choke_point(row, column, level): return True

        if self.check_for_general_choke_point(row, column, level): return True

        return False
    
    #
    #
    #
    def check_for_candidate(self, row: int, column: int, level, opponent_type: str) -> bool:

        return (
            
            row > 0 
            
            and 
            
            row < 15 
            
            and 
            
            level[row - 1, column] == '.' and
                
            # Checks whether the current tile is a solid one
            # in order to make sure that an opponent is not
            # spawned in mid air.
            self.check_tile(level[row, column]) and

            # Checks whether the selected opponent type can
            # be spawned at the current location.
            self.check_position(row, column, level, opponent_type) and not 
            
            # Makes sure that the current tile is not already
            # occupied by a previously placed opponent.
            self.check_for_opponents(row, column, level)

        )

    def check_for_bottom_row_choke_point(self, row: int, column: int, level) -> bool:

        if row != 14: return False

        return level[row, column - 1] == '.' or level[row, column + 1] == '.'



    def check_for_general_choke_point(self, row: int, column: int, level) -> bool:

        first_one_found: bool = False
        second_one_ready_to_be_found: bool = False
        second_one_found: bool = False

        for tile in level[:, column]:

            if tile != '.' and not first_one_found: first_one_found = True
            if tile == '.' and first_one_found and not second_one_ready_to_be_found: second_one_ready_to_be_found = True
            if tile != '.' and second_one_ready_to_be_found: second_one_found = True

        if second_one_found: return False

        return (
            
            (level[row + 0, column - 1] == '.' and level[row + 1, column - 1] == '.') or
            (level[row + 0, column + 1] == '.' and level[row + 1, column + 1] == '.')
        
        )


    def check_position(self, row: int, column: int, level: [[str]], opponent_type: str) -> bool:

        if opponent_type == 'C': is_valid = self.check_positions_for_opponent_type_1(row, column, level)
        if opponent_type == 'J': is_valid = self.check_positions_for_opponent_type_2(row, column, level)
        if opponent_type == 'F': is_valid = self.check_positions_for_opponent_type_3(row, column, level)
        
        return is_valid

    #
    #
    #
    def check_positions_for_opponent_type_1(self, row: int, column: int, level: [[str]]) -> bool:

        if column + 1 > (len(level[0]) - 2): return False

        return (
            
            level[row - 1, column - 1] == '.' and self.check_tile(level[row, column - 1]) and
            level[row - 1, column + 1] == '.' and self.check_tile(level[row, column + 1])
        
        )


    #
    #
    #
    def check_positions_for_opponent_type_2(self, row: int, column: int, level: [[str]]) -> bool:

        return (
            
            level[row - 4, column] == '.'  and 
            level[row - 3, column] == '.'  and 
            level[row - 2, column] == '.'  and 
            level[row - 1, column] == '.'  and
            self.check_tile(level[row, column]
        
        ))

    #
    #
    #
    def check_positions_for_opponent_type_3(self, row: int, column: int, level: [[str]]) -> bool:

        return (

            level[row - 6, column] == '.'  and 
            level[row - 5, column] == '.'  and 
            level[row - 4, column] == '.'  and 
            level[row - 3, column] == '.'  and 
            level[row - 2, column] == '.'  and 
            level[row - 1, column] == '.'

        )


    def check_tile(self, tile: str) -> bool:

        return tile == 'X' or tile == 'D' or tile == 'B' or tile == 'S'

    def check_for_opponents(self, row: int, column: int, level: [[str]]) -> bool:

        return (
                
            level[row - 0, column] == 'C' or 
            level[row - 1, column] == 'C'
        
            or 
            
            level[row - 0, column] == 'J' or 
            level[row - 1, column] == 'J'
            
            or 
            
            level[row - 0, column] == 'F' or 
            level[row - 1, column] == 'F' or
            level[row - 2, column] == 'F' or
            level[row - 3, column] == 'F' or
            level[row - 4, column] == 'F' or
            level[row - 5, column] == 'F'
        
        )

if __name__ == "__main__":

    print(Evolution().execute('user_001'))

