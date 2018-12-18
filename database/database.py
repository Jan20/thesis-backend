import sys

sys.path.append("..")

# from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, firestore

from models.performance import Performance


############################
## Production Environment ##
############################
# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred, {
#   'projectId': 'thesis-002',
# })

# db = firestore.client()

######################
## Test Environment ##
######################
cred = credentials.Certificate('../config/service_account.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

#
# Manages the the read and write operations
# to a firestore database.
#
class Database(object):

    #
    # Returns the key values under which
    # users are identified at Firestore.
    #
    def get_user_keys(self) -> [str]:

        #
        # String array intended to by filled
        # which user keys following a scheme
        # like 'user_001' or 'user_042'.
        #
        user_keys: [str] = []
        
        #
        # Iterates over all entries of the
        # 'users' collection of the referenced
        # Firestore database.
        #
        for doc in db.collection('users').get():

            #
            # Adds all document ids to the
            # previously initialized array.
            #
            user_keys.append(doc.id)

        #
        # Returns all user keys.
        #
        return user_keys

    #
    # Returns all session keys that are
    # stored for a specific user.
    #
    def get_session_keys(self, user_key: str) -> [str]:
        
        #
        # String array intended to by filled
        # which session keys following a scheme
        # like 'session_006' or 'session_134'.
        #
        session_keys: [str] = []

        #
        # Iterates over all entries of the
        # 'sessions' collection of the given
        # user document.
        #
        for doc in db.collection('users/' + user_key + '/sessions').get():
    
            #
            # Adds all document ids to the
            # previously initialized array.
            #
            session_keys.append(doc.id)

        #
        # Returns all session keys.
        #
        return session_keys

    #
    # Returns the gameplay data of a specific
    # session for a given user.
    #
    def get_performance(self, user_key: str, session_key: str) -> Performance:

        #
        # Creates a reference to the 'performance' Firestore document.
        #
        ref = db.document('users/' + user_key + '/sessions/' + session_key + '/data/performance')

        #
        # Stores all datapoints stored at the document
        # to a dictionary.
        #
        dict = ref.get().to_dict()

        #
        # Returns a Performance object created from the
        # values stored in the dictionary.
        #
        return Performance.from_dict(dict)


    #
    # Writes the users average performance
    # to the Firestore database.
    #
    def set_average_performance(self, userKey: str, average_performance: Performance) -> None:        
        
        #
        # Creates a reference to the 'average_performance' Firestore document.
        #
        ref = db.document('users/' + userKey + '/properties/average_performance')

        #
        # Writes the average performance with all
        # correspoinding attributes to Firestore.
        #
        ref.set(average_performance.to_dict())

    #
    # Retrieves the user's average performance
    # from Firestore and computes a corresponding
    # Performance object.
    #
    def get_average_performance(self, user_key: str) -> Performance:

        #
        # Creates a reference to the 'performance' Firestore document.
        #
        ref = db.document('users/' + user_key + '/properties/average_performance')

        #
        # Stores all datapoints stored at the document
        # to a dictionary.
        #
        dict = ref.get().to_dict()

        #
        # Returns a Performance object created from the
        # values stored in the dictionary.
        #
        return Performance.from_dict(dict)
    
    #
    # Stores a reference to the cluster at which a user
    # belongs to at Firestore. 
    #
    def store_cluster_membership(self, user_key, cluster_membership) -> None:

        #
        # Creates a reference to the 'cluster_membership'
        # document at Firestore.
        #
        ref = db.document('users/' + user_key + '/properties/cluster_membership')

        #
        # Write the attribute 'cluster_membership' to the
        # referenced document.
        #
        ref.set({'cluster_key': cluster_membership})

    #
    # Stores a cluster that is charactarized by its
    # centroid at Firestore.
    #
    def store_cluster(self, cluster_id: int, centroid: [float]) -> None:

        #
        # Creates a new player performance object from
        # the 'centroid' parameter that should be of  
        # the form of an array of Float values. This in-
        # between step is not strictly necessary, but keeps
        # the amount of boilerplate could to a minimum since
        # a 'Performance' object can easily converted to a
        # dictionary that can directly be stored at Firebase.
        #
        performance: Performance = Performance.from_array(centroid)

        #
        # Creates a new reference to a cluster document
        # at Firestore which is used to store a cluster's
        # centroid.
        #
        ref = db.document('clusters/cluster_00' + str(cluster_id))

        #
        # Stores the priviously created performance object
        # to Firestore by converting the obejct to a 
        # dictionary.
        #
        ref.set(performance.to_dict())
 