from models.performance import Performance

class Session(object):
    
    ##################
    ## Constructors ##
    ##################
    def __init__(self, session_key: str, session_id: int, status: str, timestamp, performance: Performance):
      
        self.session_key: str = session_key
        self.session_id: int = session_id
        self.status: str = status
        self.timestamp = timestamp
        self.performance: Performance = performance

    @staticmethod
    def from_dict(source: dict, performance: Performance):
        
        return Session(
            
            source['key'], 
            source['id'], 
            source['status'], 
            source['timestamp'], 
            performance

        )


    def to_dict(self) -> dict:

        return {

            'key': self.session_key,
            'id': self.session_id,
            'status': self.status,
            'timestamp': self.timestamp
        
        }