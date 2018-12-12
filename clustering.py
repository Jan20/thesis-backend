from database import Database
from sklearn.cluster import KMeans
import numpy as np

class Clustering(object):
    
    ##################
    ## Constructors ##
    ##################

    ###############
    ## Functions ##
    ############### 
    def test(self) -> str:

        X = np.array([[1, 2], [1, 4], [1, 0], [4, 2], [4, 4], [4, 0]])
        
        kmeans = KMeans(n_clusters=1, random_state=0).fit(X)
        
        print(kmeans.labels_)
        print(kmeans.predict([[0, 0], [4, 4]]))
        return str(kmeans.cluster_centers_)

    #
    #
    #
    #
    def cluster_users(self):   

        # Creates a database object that
        # is used across all functions.
        database = Database()

        # Stores all available user keys in the user
        # variable.
        user_keys = database.get_user_keys()

        print(user_keys)
        #
        # Defines an 
        #         
        performances = []

        for user_key in user_keys:

            average_performance = database.get_average_performance(user_key)
            
            # if average_performance is not None:

            performances.append([
                
                average_performance.get_total_deaths(),
                average_performance.get_deaths_through_gaps(),
                average_performance.get_deaths_through_opponents(),    
            
            ])

        print(performances)

        kmeans = KMeans(n_clusters=1, random_state=0).fit(performances)
        
        print(kmeans.labels_)
        # print(kmeans.predict([[0, 0], [4, 4]]))
        print(str(kmeans.cluster_centers_))    
        
        return str(kmeans.cluster_centers_)