import pandas as pd
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.performance import Performance

class User(object):
    
    ##################
    ## Constructors ##
    ##################
    def __init__(self, user_key, user_id):
      
        self.user_key: str = user_key
        self.user_id: int = user_id
      
    ###############
    ## Functions ##
    ###############
    @staticmethod
    def from_dict(source: dict):
        
        user = User(
            
            user_key=source['user_key'],
            user_id=source['user_id']
        
        )

        return user

    def to_dict(self) -> dict:

        dictionary: dict = {

            'user_key': self.user_key,
            'user_id': self.user_id
            
        }

        return dictionary
