import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.level import Level
from evolution.evolution import Evolution
from database.database import Database
from tests.samples import Samples

#
#
#
def set_up():

    database: Database = Database()

    database.store_user(Samples.sample_user)
    database.store_session(Samples.sample_user.user_key, Samples.sample_session)
    database.store_level(Samples.sample_user.user_key, Samples.sample_session.session_key, Samples.sample_level)

def clean_up():

    database: Database = Database()

    user_keys: [str] = database.get_user_keys()

    for user_key in user_keys:

        session_keys: [str] = database.get_session_keys(user_key)

        for session_key in session_keys:

            database.delete_session(user_key, session_key)

    database.delete_users()

def set_up_training_data():

    database: Database = Database()

    database.store_user(Samples.sample_user_1)
    database.store_user(Samples.sample_user_2)
    database.store_user(Samples.sample_user_3)
    database.store_user(Samples.sample_user_4)

    database.store_session(Samples.sample_user_1.user_key, Samples.sample_session_1)
    database.store_session(Samples.sample_user_1.user_key, Samples.sample_session_2)
    database.store_session(Samples.sample_user_1.user_key, Samples.sample_session_3)
    database.store_session(Samples.sample_user_2.user_key, Samples.sample_session_4)
    database.store_session(Samples.sample_user_2.user_key, Samples.sample_session_5)
    database.store_session(Samples.sample_user_3.user_key, Samples.sample_session_6)
    database.store_session(Samples.sample_user_3.user_key, Samples.sample_session_7)
    database.store_session(Samples.sample_user_4.user_key, Samples.sample_session_8)

if __name__ == "__main__":
    
    clean_up()
    set_up_training_data()