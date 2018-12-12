import datetime
from gameplay_data import Gameplay_Data

############################
## Production Environment ##
############################
# from google.cloud import firestore

######################
## Test Environment ##
######################
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./service_account.json')
firebase_admin.initialize_app(cred)

db = firestore.Client()


# Manages the the read and write operations
# to a firestore database.
class Database(object):
    

    # Returns the key values under which
    # users are identified at firestore.
    def get_user_keys(self):

        userKeys = []
        
        for doc in db.collection('users').get():

            userKeys.append(str(doc.id))

        return userKeys

    # Returns all session keys that are
    # stored for a specific user.
    def get_session_keys(self, userKey):
        

        sessionKeys = []

        for doc in db.collection('users/' + userKey + '/sessions').get():
    
            sessionKeys.append(str(doc.id))

        return sessionKeys

    # Returns the gameplay data of a specific
    # session for a given user.
    def get_gameplay_data(self, user_key, session_key):


        dict = db.document('users/' + user_key + '/sessions/' + session_key + '/data/gameplayData').get().to_dict()

        # return Gameplay_Data(
    
        #     total_deaths = dict['totalDeaths'],
        #     deaths_through_gaps = dict['deathsThroughGaps'],
        #     deaths_through_opponents = dict['deathsThroughOpponents']

        # )


    def set_average_performance(self, 
        
        userKey, 
        average_total_deaths, 
        average_deaths_through_gaps, 
        average_deaths_through_opponents 
        
        ):        
        

        db.document('users/' + userKey).set({

            'averageTotalDeaths': average_total_deaths,
            'averageDeathsThroughGaps': average_deaths_through_gaps,
            'averageDeathsThroughOpponents': average_deaths_through_opponents

        })

    def get_average_performance(self, user_key):


        dict = db.document('users/' + user_key).get().to_dict()

        return Gameplay_Data(
    
            total_deaths = dict['averageTotalDeaths'],
            deaths_through_gaps = dict['averageDeathsThroughGaps'],
            deaths_through_opponents = dict['averageDeathsThroughOpponents']

        )

    
    # def set_clusters(self, clusters):
    
    #     for user_key in user_keys:
    

    #     db.document('clusters/userCluster').set({

    #         'averageTotalDeaths': average_total_deaths,
    #         'averageDeathsThroughGaps': average_deaths_through_gaps,
    #         'averageDeathsThroughOpponents': average_deaths_through_opponents

    #     })