import os, sys

import firebase_admin
from firebase_admin import credentials, firestore
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
cred = credentials.Certificate(os.path.join(SITE_ROOT, "../config", "test_account.json"))
firebase_admin.initialize_app(cred)
db = firestore.client()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helper.helper import Helper
from models.user import User
from models.session import Session
from models.performance import Performance
from models.level import Level

import random

#
# Manages the the read and write operations
# to a firestore database.
#
class Database(object):

    ############################
    ## User Related Functions ##
    ############################
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

    

    def get_user(self, user_key: str) -> User:

        ref = db.document('users/' + user_key)

        user: User = User.from_dict(ref.get().to_dict())

        return user

    #
    #
    #
    def store_user(self, user: User) -> None:

        ref = db.document('users/' + user.user_key)

        ref.set(user.to_dict())

    #
    #
    #
    def delete_users(self) -> None:
    
        user_keys: [str] = self.get_user_keys()

        for user_key in user_keys:

            self.delete_user(user_key)

    #
    #
    #
    def delete_user(self, user_key: str) -> None:

        #
        #
        #
        ref = db.document('users/' + user_key)

        #
        #
        #
        ref.delete()

    ###############################
    ## Session Related Functions ##
    ###############################
    #
    # Retrieves a single session from Firestore.
    #
    def get_session(self, user_key: str, session_key: str) -> Session:

        #
        # Sets up a document reference to a specified session.
        #
        ref = db.document(f'users/{user_key}/sessions/{session_key}')

        #
        # Converts the entries stored within the referenced document
        # into a dictionary.
        #
        session_dict: dict = ref.get().to_dict()

        #
        # Builds up a reference to the performance document of a
        # specified session.
        #
        ref = db.document(f'users/{user_key}/sessions/{session_key}/data/performance')

        #
        # Adds the performance entries to the session dictionary, 
        # enabling the convertion from a dictionary to a Session
        # object. 
        #
        session_dict.update(ref.get().to_dict())

        #
        # Creates a session which is based on the entries within the
        # previously updated dictionary.
        #
        session: Session = Session.from_dict(session_dict)

        #
        # Return the newly created session.
        #
        return session

    #
    # Stores a new session to Firestore.
    #
    def store_session(self, user_key: str, session: Session) -> None:

        #
        # Creates a reference to a new session document.
        #
        ref = db.document(f'users/{user_key}/sessions/{session.session_key}')

        #
        # Sets all general entries to the previously referred document
        #
        ref.set({

            'key': session.session_key,
            'id': session.session_id,
            'status': session.status

        })

        #
        # Creates a reference to the peformance document of the newly created session.
        #
        ref = db.document(f'users/{user_key}/sessions/{session.session_key}/data/performance')

        #
        # Stores the performance attributes within in the previously referred document.
        #
        ref.set(session.performance.to_dict())

    #
    # 
    #
    def generate_session(self, user_key: str, level: Level) -> str:

        session_id: int = 0

        #
        #
        #
        session_ids: [int] = self.get_session_ids(user_key)

        #
        # If there are not sessions yet stored for a given user.
        #
        if len(session_ids) > 0:

            #
            #
            #
            session_id: int = max(session_ids) + 1
            
        #
        #
        #
        session_key: str = Helper().generate_key('session', session_id)
        
        ref = db.document(f'users/{user_key}/sessions/{session_key}')

        ref.set({

            'key': session_key,
            'id': session_id,
            'status': 'created'

        })

        ref = db.document(f'users/{user_key}/sessions/{session_key}/data/level')

        ref.set(level.to_dict())

        return session_key

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
        for doc in db.collection(f'users/{user_key}/sessions').get():
    
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
    # Retrieves the ids of all sessions related 
    # to a user.
    #
    def get_session_ids(self, user_key: str) -> [int]:

        #
        # String array intended to by filled
        # which session ids.
        #
        session_ids: [int] = []

        #
        # Iterates over all entries of the
        # 'sessions' collection of the given
        # user document.
        #
        for doc in db.collection(f'users/{user_key}/sessions').get():
         
            #
            # Stores all datapoints stored at the document
            # to a dictionary.
            #
            session_dict: dict = doc.to_dict()

            #
            # Retrieves the session id from the previously
            # created session dictionary.
            #
            session_ids.append(session_dict['id'])

        #
        # Returns all session ids.
        #
        return session_ids
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
    
    ###############################
    ## Cluster Related Functions ##
    ###############################
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
 
    ###########
    ## Level ##
    ###########
    #
    #
    #
    def get_generic_level(self, level_key: str) -> Level:
        
        ref = db.document('levels/' + level_key)

        #
        # Stores all datapoints stored at the document
        # to a dictionary.
        #
        dict = ref.get().to_dict()

        print('________________________________________________________________________________________')
        print(dict)

        #
        # Returns a Performance object created from the
        # values stored in the dictionary.
        #
        return Level.from_dict(dict)

    #
    #
    #
    #
    def get_level(self, user_key: str, session_key: str, level_key: str) -> Level:

        ref = db.document('users/' + user_key + '/sessions/' + session_key + '/data/level')

        dictionary: dict = ref.get().to_dict()

        return Level.from_dict(dictionary)

    #
    #
    #
    #
    def store_level(self, user_key: str, session_key: str, level: Level) -> None:

        #
        #
        #
        ref = db.document('users/' + user_key + '/sessions/' + session_key + '/data/level')

        #
        #
        #
        ref.set(level.to_dict())

    #
    #
    #
    #
    def initialize_level(self, level: Level) -> None:

        #
        #
        #
        ref = db.document(f'levels/{level.key}')

        #
        #
        #
        ref.set(level.to_dict())


    def delete_level(self, user_key: str, session_key: str, level: Level) -> None:

        #
        #
        #
        ref = db.document('users/' + user_key + '/sessions/' + session_key + '/data/level')

        #
        #
        #
        ref.delete()


    def delete_initial_level(self, level_key: str) -> None:

        #
        #
        #
        ref = db.document(f'levels/{level_key}')

        #
        #
        #
        ref.delete()

    def get_random_level(self, seed: str) -> Level:

        #
        # For test purposis only.
        #
        if (seed is 'level_01'): return self.get_generic_level('level_01')

        #
        # String array intended to by filled
        # which session keys following a scheme
        # like 'session_006' or 'session_134'.
        #
        level_keys: [str] = []

        #
        # Iterates over all entries of the
        # 'sessions' collection of the given
        # user document.
        #
        for doc in db.collection('levels').get():
    
            #
            # Adds all document ids to the
            # previously initialized array.
            #
            level_keys.append(doc.id)

        #
        #
        #
        level_key: str = random.choice(level_keys)

        #
        #
        #
        level: Level = self.get_generic_level(level_key)

        #
        # Returns all session keys.
        #
        return level