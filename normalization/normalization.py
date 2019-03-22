import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database
from models.performance import Performance
from models.session import Session

class Normalization(object):

    def __init__(self):

        self.columns: [str] = [
            
            'gaps', 
            'op_1',
            'op_2',    
            'op_3',
            'score',
            'time',
            'progress',
            'difficulty'

        ]

        # Creates a new database object.
        self.db: Database = Database()

    ###############
    ## Functions ##
    ###############

    def calculate_quantiles(self, user_key) -> float:

        weights: [float] = [

            -0.25,
            -0.25,
            -0.25,
            -0.25,
            1,
            -1,
            1,
            1,

        ]
        
        df: pd.core.frame.DataFrame = self.db.get_performances()

        if len(df) is 0: return 'class_03'

        df: pd.core.frame.DataFrame = self.calculate_average_performances(df)

        df: pd.core.frame.DataFrame = self.normalize_performances(df)

        skill_scores = (
            
            weights[0] * df['gaps'] +
            weights[1] * df['op_1'] +
            weights[2] * df['op_2'] +
            weights[3] * df['op_3'] +
            weights[4] * df['score'] +
            weights[5] * df['time'] +
            weights[6] * df['progress'] +
            weights[7] * df['difficulty']

        )
        print(df)
        quintile1: str = np.percentile(skill_scores, 20)
        quintile2: str = np.percentile(skill_scores, 40)
        quintile3: str = np.percentile(skill_scores, 60)
        quintile4: str = np.percentile(skill_scores, 80)
        quintile5: str = np.percentile(skill_scores, 100)

        columns: [str] = ['difficulty_class']

        # Defines a new dataframe intended to store 
        # the difficulty class in which a user is
        # sorted in.
        df = pd.DataFrame(columns=columns).astype(float)

        difficulty_class: str = 'class_03'

        # Iterates over all elements of the skill_scores
        # dataframe.
        for index, score in enumerate(skill_scores):

            if (score <= quintile1):   difficulty_class = 'class_01'
            elif (score <= quintile2): difficulty_class = 'class_02'
            elif (score <= quintile3): difficulty_class = 'class_03'
            elif (score <= quintile4): difficulty_class = 'class_04'
            elif (score <= quintile5): difficulty_class = 'class_05'
            
            df = df.append(pd.DataFrame([difficulty_class], columns=columns, index=[skill_scores.index.values[index]]))

        return df.iloc[0]['difficulty_class']
    
    #
    #
    #
    def normalize_performances(self, input: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:

        # Creates an empty dataframe. 
        df = pd.DataFrame(columns=self.columns).astype(float)
        
        if len(input) is 0: return df

        # If either none or just one user is stored so far,
        if len(input) is 1:

            # Converts the entries of the dataframe to a list.
            a = np.array(input.values.tolist())
            
            # Replaces all values that are greater than one by one.
            normalizeed_performance = np.where(a > 1, 1, a).tolist()

            # 

            df = pd.DataFrame(normalizeed_performance, columns=self.columns, index=[input.iloc[0].name])

        else:
            
            df = input.fillna(0)
            df -= df.min()  # equivalent to df = df - df.min()

            df /= df.max()  # equivalent to df = df / df.max()



        df = input.fillna(0)

        return df
        
    # 
    # Calculates the average gameplay performance
    # over all previously played sessions for a
    # particular user.
    #
    def calculate_average_performances(self, input: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:

        # Creates a dataframe holding all sessions
        # played by a given user.
        df = pd.DataFrame(columns=self.columns).astype(float)

        temp_df = pd.DataFrame(columns=self.columns).astype(float)

        current_user: str = input.iloc[0].name

        for i, _ in enumerate(np.array(input)):
            
            user = input.iloc[i].name

            if current_user == user:

                temp_df = temp_df.append(input.iloc[i])
                
            else:

                mean = temp_df.mean()
                
                temp_df = pd.DataFrame(columns=self.columns).astype(float)

                df = df.append(pd.DataFrame([mean], columns=self.columns, index=[current_user]))

                current_user = user



        mean = temp_df.mean()
        
        temp_df = pd.DataFrame(columns=self.columns).astype(float)

        df = df.append(pd.DataFrame([mean], columns=self.columns, index=[current_user]))
        # Write a user's average performance to Firestore. 
        # self.db.set_average_performance(user_key, performance)
        # Returns the average performance.

        return df



if __name__ == "__main__":

    pass
    # db = Database()
