import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Level:
    
    #################
    ## Constructor ##
    #################
    def __init__(self, key: str, id: int, representation: [[str]]):

        self.key: str = key
        self.id: int = id
        self.representation: [[str]] = representation 


    ###############
    ## Functions ##
    ###############
    @staticmethod
    def from_dict(source: dict):
        
        level = Level(
            
            key = source['key'],
            id = source['id'],

            representation = [
                
                source['line_00'],
                source['line_01'],
                source['line_02'],
                source['line_03'],
                source['line_04'],
                source['line_05'],
                source['line_06'],
                source['line_07'],
                source['line_08'],
                source['line_09'],
                source['line_10'],
                source['line_11'],
                source['line_12'],
                source['line_13'],
                source['line_14']
                
            ]

        )

        return level


    def to_dict(self) -> dict:
     
        dictionary: dict = {

            'key': self.key,
            'id': self.id,
            'line_00': self.representation[0],
            'line_01': self.representation[1],
            'line_02': self.representation[2],
            'line_03': self.representation[3],
            'line_04': self.representation[4],
            'line_05': self.representation[5],
            'line_06': self.representation[6],
            'line_07': self.representation[7],
            'line_08': self.representation[8],
            'line_09': self.representation[9],
            'line_10': self.representation[10],
            'line_11': self.representation[11],
            'line_12': self.representation[12],
            'line_13': self.representation[13],
            'line_14': self.representation[14]

        }

        return dictionary