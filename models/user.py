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
            
            source['user_key'],
            source['user_id']
        
        )

        return user

    def to_dict(self) -> dict:

        dictionary: dict = {

            'user_key': self.user_key,
            'user_id': self.user_id
            
        }

        return dictionary
