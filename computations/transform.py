import sys

sys.path.append("..")

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from database.database import Database
from models.performance import Performance

class Transform(object):

    ###############
    ## Functions ##
    ###############
    
    # 
    # Calculates the average gameplay performance
    # over all previously played sessions for a
    # particular user and stores the results in a
    # Firestore database.
    #
    def calculate_average_performance(self, user_key: str) -> str:

        #
        # Creates a new database object.
        #
        database: Database = Database()

        # 
        # Retrieves all session keys relating to
        # game sessions played by an user.
        #
        session_keys: [str] = database.get_session_keys(user_key)

        #
        # Sets up a range of empty arrays
        # intended to store all gameplay related
        # datapoints.
        #
        defeated_by_gaps: [float] = []
        defeated_by_opponent_type_1: [float] = []
        defeated_by_opponent_type_2: [float] = [] 
        defeated_by_opponent_type_3: [float] = []

        #
        # Iterates over all sessions played
        # by an user.
        #        
        for session_key in session_keys:

            #
            # Stores all gameplay related data from a 
            # given user and session in a temporary variable.
            #
            performance: Performance = database.get_performance(user_key, session_key)
            
            #
            # Appends the recently retrieved gameplay related
            # datapoints to their respective arrays.
            #
            defeated_by_gaps.append(performance.defeated_by_gaps)
            defeated_by_opponent_type_1.append(performance.defeated_by_opponent_type_1)
            defeated_by_opponent_type_2.append(performance.defeated_by_opponent_type_2)
            defeated_by_opponent_type_3.append(performance.defeated_by_opponent_type_3)


        #
        # Computes the average value of every previously
        # created and filled arrays. 
        # 
        average_performance: Performance = Performance(
            
            np.average(defeated_by_gaps),
            np.average(defeated_by_opponent_type_1),
            np.average(defeated_by_opponent_type_2),
            np.average(defeated_by_opponent_type_3)

        )

        #
        # The result is then
        # written into a Firestore database.   
        #
        database.set_average_performance(user_key, average_performance)

        return 'done'
