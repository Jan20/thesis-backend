import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.level import Level

class Helper(object):

    #
    # Generates a key value based on a key_word as well as
    # an id value.
    #
    @staticmethod
    def generate_key(key_word: str, id: int) -> str:
        
        # Checks wether the user id is smaller than
        # ten leading to a result like 'user004'.
        if (id < 10): return f'{key_word}_00{id}'

        # If the user id is smaller than 100, a user
        # key like 'user095' should be returned.
        if (id < 100): return f'{key_word}_0{id}'

        # By default, an generic user key should
        # be returned. 
        return f'{key_word}_{id}'

    @staticmethod
    def clean_level(level: Level) -> Level:

        for i in range(len(level.representation)):

            for j in range(len(level.representation[i])):

                if level.representation[i][j] == 'C':

                    level.representation[i][j] = '.'

        return level
    