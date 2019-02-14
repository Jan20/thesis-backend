import os
import sys
from math import floor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import preprocessing

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
        self.database: Database = Database()

    ###############
    ## Functions ##
    ###############

    def calculate_user_score(self, user_key) -> float:

        weights: [float] = [

            -0.25,
            -0.25,
            -0.25,
            -0.25,
            1,
            -2,
            2.5,
            0.25

        ]
        
        df = self.normalize_performance()
        
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

        if skill_scores[user_key] < 0.3:

            skill_scores[user_key] = 0.3

        return floor(skill_scores[user_key] * 100)

    #
    #
    #
    def normalize_performance(self) -> pd.core.frame.DataFrame:

        # Retrieves the keys for all users stored at Firestore. 
        user_keys: [str] = self.database.get_user_keys()

        df = pd.DataFrame(columns=self.columns).astype(float)
        
        for user_key in user_keys:
            
            df = df.append(self.calculate_average_performance(user_key))

        if len(user_keys) < 2:
            
            a = np.array(df.values.tolist())

            array = np.where(a > 1, 1, a).tolist()

            df = pd.DataFrame(array, columns=self.columns, index=[f'{user_key}'])

        else:
        
            df -= df.min()  # equivalent to df = df - df.min()
            df /= df.max()

        return df
        


    # 
    # Calculates the average gameplay performance
    # over all previously played sessions for a
    # particular user.
    #
    def calculate_average_performance(self, user_key: str) -> pd.core.frame.DataFrame:

        # Creates a dataframe holding all sessions
        # played by a given user.
        df = self.create_DataFrame(user_key)

        # Computes the mean of all sessions.
        mean = df.mean()

        performance: Performance = Performance(
            
            mean['gaps'],
            mean['op_1'],
            mean['op_2'],
            mean['op_3'],
            mean['score'],
            mean['time'],
            mean['progress'],
            mean['difficulty']
        
        )

        # Write a user's average performance to Firestore. 
        # self.database.set_average_performance(user_key, performance)

        # Returns the average performance.
        return pd.DataFrame([performance.to_array()], columns=self.columns, index=[f'{user_key}'])


    #
    # Creates dataframe storing the all performance
    # related attributes of all sessions played by 
    # a given user.
    #
    def create_DataFrame(self, user_key: str) -> pd.core.frame.DataFrame:

        # Initializes an empty dataframe with float values.
        df = pd.DataFrame(columns=self.columns).astype(float)
        
        # Retrieves al session keys for a given user.
        session_keys = self.database.get_session_keys(user_key)

        # Iterates through all session keys.
        for session_key in session_keys:

            # Creates an index that identifies every
            # row of the dataframe.
            index = [f'{user_key}:{session_key}']

            # Retrieves the performance attributes of
            # a single session.
            performance: Performance = self.database.get_performance(user_key, session_key)
            
            # Appends the previously retrieved performance
            # the dataframe object defiend above.
            df = df.append(pd.DataFrame([performance.to_array()], columns=self.columns, index=index))

        # Returns the previously defind and through
        # the for-loop filled dataframe.
        return df

if __name__ == "__main__":

    test = Normalization().create_DataFrame('user_001')
