import pandas as pd

class Performance(object):
    
    ##################
    ## Constructors ##
    ##################
    def __init__(self, 
    
        defeated_by_gaps: float, 
        defeated_by_opponent_type_1: float, 
        defeated_by_opponent_type_2: float, 
        defeated_by_opponent_type_3: float,
    
    ):
        
        self.defeated_by_gaps: float = defeated_by_gaps
        self.defeated_by_opponent_type_1: float = defeated_by_opponent_type_1
        self.defeated_by_opponent_type_2: float = defeated_by_opponent_type_2 
        self.defeated_by_opponent_type_3: float = defeated_by_opponent_type_3 

    ###############
    ## Functions ##
    ###############
    @staticmethod
    def from_dict(source: dict):
        
        performance = Performance(
            
            defeated_by_gaps = source['defeated_by_gaps'],
            defeated_by_opponent_type_1 = source['defeated_by_opponent_type_1'],
            defeated_by_opponent_type_2 = source['defeated_by_opponent_type_2'],
            defeated_by_opponent_type_3 = source['defeated_by_opponent_type_3'],

        )

        return performance

    def to_dict(self) -> dict:

        dictionary: dict = {

            'defeated_by_gaps': self.defeated_by_gaps,
            'defeated_by_opponent_type_1': self.defeated_by_opponent_type_1,
            'defeated_by_opponent_type_2': self.defeated_by_opponent_type_2,
            'defeated_by_opponent_type_3': self.defeated_by_opponent_type_3,

        }

        return dictionary

    @staticmethod
    def from_array(source: [float]): 

        performance = Performance(
            
            defeated_by_gaps = source[0],
            defeated_by_opponent_type_1 = source[1],
            defeated_by_opponent_type_2 = source[2],
            defeated_by_opponent_type_3 = source[3],

        )

        return performance