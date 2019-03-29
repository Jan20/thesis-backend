class User(object):
    
    ##################
    ## Constructors ##
    ##################
    def __init__(self, user_key: str, user_id: int, language: str):
      
        self.user_key: str = user_key
        self.user_id: int = user_id
        self.language: str = language
      
    ###############
    ## Functions ##
    ###############
    @staticmethod
    def from_dict(source: dict):
        
        return User(
            
            source['user_key'],
            source['user_id'],
            source['language']
        
        )

    def to_dict(self) -> dict:

        return {

            'user_key': self.user_key,
            'user_id': self.user_id,
            'language': self.language
            
        }
