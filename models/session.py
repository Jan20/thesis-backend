import pandas as pd
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.performance import Performance

class Session(object):
    
    ##################
    ## Constructors ##
    ##################
    def __init__(self, session_key: str, session_id: int, status: str, performance: Performance):
      
        self.session_key: str = session_key
        self.session_id: int = session_id
        self.status: str = status
        self.performance: Performance = performance
      

    def to_dict(self) -> dict:

        return {

            'key': self.session_key,
            'id': self.session_id,
            'status': self.status
        
        }
