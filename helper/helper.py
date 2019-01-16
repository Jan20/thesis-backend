class Helper(object):

    def generate_key(self, key_word: str, id: int) -> str:
        
        #
        # Checks wether the user id is smaller than
        # ten leading to a result like 'user004'.
        #
        if (id < 10): return f'{key_word}_00{id}'

        #
        # If the user id is smaller than 100, a user
        # key like 'user095' should be returned.
        #
        if (id < 100): return f'{key_word}_0{id}'

        #
        # By default, an generic user key should
        # be returned. 
        #
        return f'{key_word}_{id}'
