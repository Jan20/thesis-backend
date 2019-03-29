import os, sys
import firebase_admin
from firebase_admin import credentials, firestore
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
cred = credentials.Certificate(os.path.join(SITE_ROOT, "../config", "service_account.json"))
firebase_admin.initialize_app(cred)
db = firestore.client()
server_timestamp = firestore.firestore.SERVER_TIMESTAMP

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helper.helper import Helper
from models.user import User
from models.session import Session
from models.performance import Performance
from models.level import Level

import pandas as pd

import random

#
# Manages the the read and write operations
# to a firestore database.
#
class Database(object):

    def generate_timestamp(self):

        return server_timestamp

    ############################
    ## User Related Functions ##
    ############################
    #
    # Returns the key values under which
    # users are identified at Firestore.
    #
    def get_user_keys(self) -> [str]:

        # String array intended to by filled
        # which user keys following a scheme
        # like 'user_001' or 'user_042'.
        user_keys: [str] = []
        
        # Iterates over all entries of the
        # 'users' collection of the referenced
        # Firestore database.
        for doc in db.collection('users').get():

            # Adds all document ids to the
            # previously initialized array.
            user_keys.append(doc.id)

        # Returns all user keys.
        return user_keys

    
    #
    # Returns a user object based on a given
    # user key.
    #
    def get_user(self, user_key: str) -> User:

        # Defines a reference to a user document.
        ref = db.document(f'users/{user_key}')

        # Creates a user from the data stored at
        # the user document.
        user: User = User.from_dict(ref.get().to_dict())

        # Returns the previously created user.
        return user

    #
    #
    #
    def store_user(self, user: User) -> None:

        db.document(f'users/{user.user_key}').set(user.to_dict())

    #
    #
    #
    def delete_users(self) -> None:
    
        user_keys: [str] = self.get_user_keys()

        for user_key in user_keys:

            self.delete_user(user_key)

    #
    # Deletes a single user from Firestore.
    #
    def delete_user(self, user_key: str) -> None:

        # Removes the Firestore reference of a specified user.
        db.document(f'users/{user_key}').delete()

    ###############################
    ## Session Related Functions ##
    ###############################
    #
    # Retrieves a single session from Firestore.
    #
    def get_session(self, user_key: str, session_key: str) -> Session:

        # Sets up a document reference to a specified session.
        ref = db.document(f'users/{user_key}/sessions/{session_key}')

        # Converts the entries stored within the referenced document
        # into a dictionary.
        session_dict: dict = ref.get().to_dict()

        # Builds up a reference to the performance document of a
        # specified session.
        ref = db.document(f'users/{user_key}/sessions/{session_key}/data/performance')

        # Adds the performance entries to the session dictionary, 
        # enabling the convertion from a dictionary to a Session
        # object. 
        performance: Performance = Performance.from_dict(ref.get().to_dict())

        # Creates a session which is based on the entries within the
        # previously updated dictionary.
        session: Session = Session.from_dict(session_dict, performance)

        # Return the newly created session.
        return session

    #
    # Stores a new session to Firestore.
    #
    def store_session(self, user_key: str, session: Session) -> None:
        
        # Creates a reference to a new session document.
        ref = db.document(f'users/{user_key}/sessions/{session.session_key}')

        # Sets all general entries to the previously referred document
        ref.set(session.to_dict())

        # Creates a reference to the peformance document of the newly created session.
        ref = db.document(f'users/{user_key}/sessions/{session.session_key}/data/performance')
        
        ref.set(session.performance.to_dict())

        obj: dict = session.performance.to_dict()
        obj['user_key'] = user_key
        obj['session_key'] = session.session_key

        # Stores the performance attributes within in the previously referred document.
        db.document(f'performances/{user_key}:{session.session_key}').set(obj)
        

    #
    # Creates a new session for a given user.
    #
    def generate_session(self, user_key: str, level: Level, difficulty_score: float) -> str:

        # Variable intended to store the key
        # that will be created within the function.
        session_id: int = 0

        # Fetches the ids of all previously played sessions.
        session_ids: [int] = self.get_session_ids(user_key)

        # Checks whether at least a single session has been
        # stored before for a given user.
        if len(session_ids) > 0:

            # Sets the id for the session that should be
            # created next to one higher than previous
            # session id. 
            session_id = max(session_ids) + 1
            
        # Generates a key that corresponds to the previously
        # created id like 'session_042' if the session's id
        # is '42'
        session_key: str = Helper().generate_key('session', session_id)

        # Defines a new performance object which values are
        # initialized with zeros.
        performance: Performance = Performance(0, 0, 0, 0, 0, 0, 0, difficulty_score)
        

        # Creates a new session object based on the previously
        # defined key and id pair.
        session: Session = Session(session_key, session_id, 'created', server_timestamp, performance)

        # Defines a new database reference pointing towards
        # the place at which the new session sould be stored.
        ref = db.document(f'users/{user_key}/sessions/{session_key}')

        # Writes the generated session to Firestore.
        ref.set(session.to_dict())

        # Defines a new database reference at which the session's
        # performance should be stored.
        ref = db.document(f'users/{user_key}/sessions/{session_key}/data/performance')

        # Stores the session's performance.
        ref.set(performance.to_dict())

        # Defines a new database reference pointing to the place at
        # which the level for the generated session should be stored.
        ref = db.document(f'users/{user_key}/sessions/{session_key}/data/level')

        # Stores the session's level at Firestore.
        ref.set(level.to_dict())

        # Returns the key of the generated session.
        return session_key
    
    #
    #
    #
    def delete_session(self, user_key: str, session_key: str) -> None:
        
        #
        db.document(f'users/{user_key}/sessions/{session_key}').delete()



    #
    # Returns all session keys that are
    # stored for a specific user.
    #
    def get_session_keys(self, user_key: str) -> [str]:

        # String array intended to by filled
        # which user keys following a scheme
        # like 'user_001' or 'user_042'.
        session_keys: [str] = []
        
        # Iterates over all entries of the
        # 'users' collection of the referenced
        # Firestore database.
        for doc in db.collection(f'users/{user_key}/sessions').get():

            # Adds all document ids to the
            # previously initialized array.
            session_keys.append(doc.id)

        # Returns all user keys.
        return session_keys

    #
    # Retrieves the ids of all sessions related 
    # to a user.
    #
    def get_session_ids(self, user_key: str) -> [int]:

        # String array intended to by filled
        # which session ids.
        session_ids: [int] = []

        # Iterates over all entries of the
        # 'sessions' collection of the given
        # user document.
        for doc in db.collection(f'users/{user_key}/sessions').get():
         
            # Stores all datapoints stored at the document
            # to a dictionary.
            session_dict: dict = doc.to_dict()

            # Retrieves the session id from the previously
            # created session dictionary.
            session_ids.append(session_dict['id'])

        # Returns all session ids.
        return session_ids

    def get_sessions(self) -> [Performance]:

        performances: [Performance] = []

        for doc in db.collection(f'performances').get():

            d = doc.to_dict()

            user_key = d['user_key']

            performance: Performance = Performance(
                d['defeated_by_gaps'],
                d['defeated_by_opponent_type_1'],
                d['defeated_by_opponent_type_2'],
                d['defeated_by_opponent_type_3'],
                d['score'],
                d['time'],
                d['progress'],
                d['difficulty']
            )

            if user_key != 'user_001':

                performances.append(performance)

        return performances

    #################
    ## Performance ##
    #################
    #
    # Returns the gameplay data of a specific
    # session for a given user.
    #
    def get_performance(self, user_key: str, session_key: str) -> Performance:

        # Creates a reference to the 'performance' Firestore document.
        ref = db.document(f'users/{user_key}/sessions/{session_key}/data/performance')

        # Stores all datapoints stored at the document
        # to a dictionary.
        dictionary: dict = ref.get().to_dict()

        # Returns a Performance object created from the
        # values stored in the dictionary.
        return Performance.from_dict(dictionary)

    #
    # Creates a dataframe storing all performance
    # related attributes of all sessions played by 
    # a given user.
    #
    def get_performances(self) -> pd.core.frame.DataFrame:

        # Defines the columns of the dataframe that is
        # going to be returned by the function.
        columns: [str] = [
            
            'gaps',
            'op_1',
            'op_2',
            'op_3',
            'score', 
            'time',
            'progress',
            'difficulty'

        ]

        # Defines an empty dataframe intended to store
        # the performances achieved by all users across
        # all their sessions.
        df = pd.DataFrame(columns=columns).astype(int)
        
        # Iterates over all performances stored at Firestore.
        for doc in db.collection(f'performances').get():

            # Converts the response from Firestore into a dict.
            value = doc.to_dict()
            
            # Adds a new row to the dataframe defined above.
            df = df.append(pd.DataFrame([[
            
                value['defeated_by_gaps'],
                value['defeated_by_opponent_type_1'],
                value['defeated_by_opponent_type_2'],
                value['defeated_by_opponent_type_3'],
                value['score'],
                value['time'],
                value['progress'],
                value['difficulty'],

            ]], columns=columns, index=[f'{value["user_key"]}']))


        # Returns the filled dataframe.
        return df

    #
    # Writes the users average performance
    # to the Firestore database.
    #
    def set_average_performance(self, userKey: str, average_performance: Performance) -> None:        
        
        # Creates a reference to the 'average_performance' Firestore document.
        ref = db.document(f'users/{userKey}/properties/average_performance')

        # Writes the average performance with all
        # correspoinding attributes to Firestore.
        ref.set(average_performance.to_dict())

    #
    # Retrieves the user's average performance
    # from Firestore and computes a corresponding
    # Performance object.
    #
    def get_average_performance(self, user_key: str) -> Performance:

        # Creates a reference to the 'performance' Firestore document.
        ref = db.document(f'users/{user_key}/properties/average_performance')

        # Stores all datapoints stored at the document
        # to a dictionary.
        dict = ref.get().to_dict()

        # Returns a Performance object created from the
        # values stored in the dictionary.
        return Performance.from_dict(dict)
    
    ###############################
    ## Cluster Related Functions ##
    ###############################
    #
    # Stores a reference to the cluster at which a user
    # belongs to at Firestore. 
    #
    def store_cluster_membership(self, user_key, cluster_membership) -> None:

        # Creates a reference to the 'cluster_membership'
        # document at Firestore.
        ref = db.document(f'users/{user_key}/properties/cluster_membership')

        # Write the attribute 'cluster_membership' to the
        # referenced document.
        ref.set({'cluster_key': cluster_membership})

    #
    # Stores a cluster that is charactarized by its
    # centroid at Firestore.
    #
    def store_cluster(self, cluster_id: int, centroid: [float]) -> None:

        # Creates a new player performance object from
        # the 'centroid' parameter that should be of  
        # the form of an array of Float values. This in-
        # between step is not strictly necessary, but keeps
        # the amount of boilerplate could to a minimum since
        # a 'Performance' object can easily converted to a
        # dictionary that can directly be stored at Firebase.
        performance: Performance = Performance.from_array(centroid)

        # Creates a new reference to a cluster document
        # at Firestore which is used to store a cluster's
        # centroid.
        ref = db.document(f'clusters/cluster_00{str(cluster_id)}')

        # Stores the priviously created performance object
        # to Firestore by converting the obejct to a 
        # dictionary.
        ref.set(performance.to_dict())
 
    #############################
    ## Level related functions ##
    #############################

    #
    # Retrieves a level prototype from Firestore. A level
    # prototype provides a level without any opponents.
    #
    def get_level_prototype(self, level_key: str) -> Level:
        
        # Retrieves a level prototype from Firestore.
        dictionary: dict = db.document(f'level_prototypes/{level_key}').get().to_dict()

        # Returns a level object created
        return Level.from_dict(dictionary)




    #
    #
    #
    def get_level(self, user_key: str, session_key: str, level_key: str) -> Level:

        ref = db.document(f'users/{user_key}/sessions/{session_key}/data/level')

        dictionary: dict = ref.get().to_dict()

        return Level.from_dict(dictionary)

    #
    # Stores a level for a specific session to Firestore.
    #
    def store_level(self, user_key: str, session_key: str, level: Level) -> None:

        # Defines are reference to a Firebase level document.
        ref: str = f'users/{user_key}/sessions/{session_key}/data/level'

        # Stores the level to the level document.
        db.document(ref).set(level.to_dict())


    #
    # Stores a level prototype at Firestore.
    #
    def store_level_prototype(self, level: Level) -> None:

        # Creates a new level prototype document at Firestore.
        db.document(f'level_prototypes/{level.key}').set(level.to_dict())

    #
    # Stores a level used in the tutorial
    #
    def store_tutorial(self, level: Level) -> None:

        # Creates a new turorial at Firestore.
        db.document(f'tutorials/{level.key}').set(level.to_dict())


    #
    # Stores an initial level to Firestore.
    #
    def store_initial_level(self, level: Level) -> None:

        # Creates a new level document at Firestore.
        db.document(f'levels/{level.key}').set(level.to_dict())


    #
    # 
    #
    def initialize_level_prototype(self, level: Level) -> None:

        #
        db.document(f'level_prototypes/{level.key}').set(level.to_dict())


    #
    #
    #
    def delete_level(self, user_key: str, session_key: str, level: Level) -> None:

        #
        db.document(f'users/{user_key}/sessions/{session_key}/data/level').delete()


    #
    #
    #
    def delete_initial_level(self, level_key: str) -> None:

        #
        db.document(f'levels/{level_key}').delete()


    #
    #
    #
    def get_random_level(self) -> Level:

        # String array intended to by filled
        # which session keys following a scheme
        # like 'session_006' or 'session_134'.
        level_keys: [str] = []

        # Iterates over all entries of the
        # 'sessions' collection of the given
        # user document.
        for doc in db.collection(f'levels').get():
    
            # Adds all document ids to the
            # previously initialized array.
            level_keys.append(doc.id)

        # Selects a level key randomly.
        level_key: str = random.choice(level_keys)

        # Creates a new level object.
        # TODO: Important 
        level: Level = self.get_level_prototype(level_key)
        # level: Level = self.get_level_prototype('level_04')

        # Returns all session keys.
        return level

