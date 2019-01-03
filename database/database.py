import sys
import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.append("..")

import os

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
cred = credentials.Certificate(os.path.join(SITE_ROOT, "../config", "service_account.json")
)
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
 
    ############################
    ## For test purposis only ##
    ############################
    def createUser(self) -> None:
        print('Hello')
#     // Fetches the highest existing user id and
#     // increases the value by one. This should
#     // ensure that a user id is not used twice
#     // throughtout the experiment.
#     const id: number = await this.getHighestUserId() + 1
#     const key: string = new AnalyticsHelper().generateKey('user', id)

#     // Constructs a key value for storing a new
#     // user at firestore. The key should look
#     // like 'user001'.
#     const user: User = {id: id, key: key}

#     // Creates a new entry at Firestore that 
#     // corresponds to the newly created user key.
#     await this.angularFirestore.doc(`users/${user.key}`).set(user)

#     // Sets a key-value-pair for the newly created
#     // user key at the user's localStorage.
#     localStorage.setItem('user_key', user.key)

#     // Returns a promise pointing to the just
#     // created userKey.
#     return new Promise<User>(resolve => resolve(user))

#   }

 
    def get_highest_user_id(self) -> int:
    
        # Sets a default user id.
        highest_user_id: int = 0

        # Iterates through all users from firestore and
        # compares their user ids with the one stored in
        # the highestUserId variable.
        for user in db.collection('users').get():

            print(user.to_dict())
        # dict = ref.get().to_dict()

        #     #
        #     # Adds all document ids to the
        #     # previously initialized array.
        #     #
        #     user_keys.append(doc.id)


        # If the user's id is higher than
        # the former highest user id, the
        # value of the highestUserId variable 
        # is is replaced by the one stored in
        # the userId variable.
#         user. > highest_user_id ? highest_user_id = user.data().id : null

#     // Resolves promise by returning the highest user id
#     // which should always be an number.
#     return new Promise<number>(resolve => resolve(highest_user_id))

