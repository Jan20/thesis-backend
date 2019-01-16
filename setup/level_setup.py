import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd

from models.level import Level
from database.database import Database
from setup.text_file_reader import TextFileReader

class LevelSetup(object):

    def initialize_levels(self):

        database: Database = Database()

        database.initialize_level(Level('level_01', '01', TextFileReader().read_text_file('level_01.txt')))
        database.initialize_level(Level('level_02', '02', TextFileReader().read_text_file('level_02.txt')))
        database.initialize_level(Level('level_03', '03', TextFileReader().read_text_file('level_03.txt')))
        database.initialize_level(Level('level_04', '04', TextFileReader().read_text_file('level_04.txt')))
        database.initialize_level(Level('level_05', '05', TextFileReader().read_text_file('level_05.txt')))
        database.initialize_level(Level('level_06', '06', TextFileReader().read_text_file('level_06.txt')))
        database.initialize_level(Level('level_07', '07', TextFileReader().read_text_file('level_07.txt')))
        database.initialize_level(Level('level_08', '08', TextFileReader().read_text_file('level_08.txt')))

        database.delete_initial_level('level_42')

if __name__ == "__main__":

    LevelSetup().initialize_levels()