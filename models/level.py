import os,sys
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
                
                list(source['line_00']),
                list(source['line_01']),
                list(source['line_02']),
                list(source['line_03']),
                list(source['line_04']),
                list(source['line_05']),
                list(source['line_06']),
                list(source['line_07']),
                list(source['line_08']),
                list(source['line_09']),
                list(source['line_10']),
                list(source['line_11']),
                list(source['line_12']),
                list(source['line_13']),
                list(source['line_14'])
                
            ]

        )

        return level


    def to_dict(self) -> dict:
     
        dictionary: dict = {

            'key': self.key,
            'id': self.id,
            'line_00': ''.join(self.representation[0]),
            'line_01': ''.join(self.representation[1]),
            'line_02': ''.join(self.representation[2]),
            'line_03': ''.join(self.representation[3]),
            'line_04': ''.join(self.representation[4]),
            'line_05': ''.join(self.representation[5]),
            'line_06': ''.join(self.representation[6]),
            'line_07': ''.join(self.representation[7]),
            'line_08': ''.join(self.representation[8]),
            'line_09': ''.join(self.representation[9]),
            'line_10': ''.join(self.representation[10]),
            'line_11': ''.join(self.representation[11]),
            'line_12': ''.join(self.representation[12]),
            'line_13': ''.join(self.representation[13]),
            'line_14': ''.join(self.representation[14])

        }

        return dictionary