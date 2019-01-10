import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from database.database import Database
from models.performance import Performance


class Cluster(object):
    
    ###############
    ## Functions ##
    ############### 
    def __init__(self):
        
        #
        # Creates a database object that
        # is used across all functions.
        #
        self.database = Database()

    #
    # Performs the clustering of users according
    # to their average performances.
    #
    def cluster_users(self) -> str:   

        #
        # Retrieves all user keys from Firestore.
        #
        user_keys: [str] = self.database.get_user_keys()

        #
        # Initializes an empty array intended
        # to store 
        #
        average_performances = pd.DataFrame(self.database.get_average_performance(user_keys[0]).to_dict(), index=[user_keys[0]])

        user_key_of_first_user = user_keys[0]
        user_keys.remove(user_keys[0])

        #
        # Iterates over all user keys.
        #
        for user_key in user_keys:

            #
            # Retrieves the average_performance of the
            # current user.
            #
            average_performance: Performance = self.database.get_average_performance(user_key)
            
            ################
            ## TODO: Ugly ##
            ################
            if average_performance is not None:

                #
                # Pushes the average_performance object
                # of every user to the average_performances
                # array.
                #
                df = pd.DataFrame(self.database.get_average_performance(user_keys[0]).to_dict(), index=[user_key])
                average_performances = average_performances.append(df)
        #
        # Creates a four clusters based on the users
        # average performances.
        #
        user_keys = [user_key_of_first_user] + user_keys

        number_of_clusters: int = 2

        kmeans = KMeans(n_clusters=number_of_clusters, random_state=0).fit(average_performances)

        cluster_ids: [int] = []
        
        for i in range(number_of_clusters):

            cluster_ids.append(i)

        self.store_clusters(cluster_ids, kmeans.cluster_centers_)

        self.store_clusters_to_users(user_keys, kmeans.labels_)
        
        return str(kmeans.cluster_centers_)


    def store_clusters(self, cluster_ids: [int], centroids):

        for index, cluster_id in enumerate(cluster_ids):

            self.database.store_cluster(cluster_id, centroids[index])


    #
    #
    #
    def store_clusters_to_users(self, user_keys: [str], cluster_labels):
        
        for index, item in enumerate(user_keys):

            self.database.store_cluster_membership(user_keys[index], int(cluster_labels[index]))

    