import pandas as pd
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.performance import Performance

class Session(object):
    
    ##################
    ## Constructors ##
    ##################
    def __init__(self, session_key: str, session_id: int, performance: Performance):
      
        self.session_key: str = session_key
        self.session_id: int = session_id
        self.performance: Performance = performance
      
    ###############
    ## Functions ##
    ###############
    @staticmethod
    def from_dict(source: dict):
        
        session = Session(
            
            session_key = source['session_key'],
            session_id = source['session_id'],
            performance = Performance(
                
                source['defeated_by_gaps'],
                source['defeated_by_opponent_type_1'],
                source['defeated_by_opponent_type_2'],
                source['defeated_by_opponent_type_3']
                
            )
        )

        return session

    def to_dict(self) -> dict:

        dictionary: dict = {

            'session_key': self.session_key,
            'session_id': self.session_id,
            'data': {
                
                'performance': {
            
                'defeated_by_gaps': self.performance.defeated_by_gaps,
                'defeated_by_opponent_type_1': self.performance.defeated_by_opponent_type_1,
                'defeated_by_opponent_type_2': self.performance.defeated_by_opponent_type_2,
                'defeated_by_opponent_type_3': self.performance.defeated_by_opponent_type_3,

                }
            
            }
            
        }

        return dictionary
