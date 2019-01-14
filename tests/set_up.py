import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.level import Level
from evolution.evolution import Evolution
from database.database import Database
from tests.samples import Samples

def set_up():

    database: Database = Database()

    database.store_user(Samples.sample_user)
    database.store_session(Samples.sample_user.user_key, Samples.sample_session)
    database.store_level(Samples.sample_user.user_key, Samples.sample_session.session_key, Samples.sample_level)

def clean_up():

    Database().delete_users()

if __name__ == "__main__":
    
    set_up()