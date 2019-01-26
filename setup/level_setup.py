import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd

from models.level import Level
from database.database import Database
from setup.text_file_reader import TextFileReader
from helper.helper import Helper
from evolution.evolution import Evolution

class LevelSetup(object):

    def initialize_levels(self):

        database: Database = Database()
        evolution: Evolution = Evolution()

        level_01: Level = Level('level_01', '01', TextFileReader().read_text_file('level_01.txt'))
        level_02: Level = Level('level_02', '02', TextFileReader().read_text_file('level_02.txt'))
        level_03: Level = Level('level_03', '03', TextFileReader().read_text_file('level_03.txt'))
        level_04: Level = Level('level_04', '04', TextFileReader().read_text_file('level_04.txt'))
        level_05: Level = Level('level_05', '05', TextFileReader().read_text_file('level_05.txt'))
        level_06: Level = Level('level_06', '06', TextFileReader().read_text_file('level_06.txt'))
        level_07: Level = Level('level_07', '07', TextFileReader().read_text_file('level_07.txt'))
        level_08: Level = Level('level_08', '08', TextFileReader().read_text_file('level_08.txt'))
        
        level_01 = Helper.clean_level(level_01)
        level_02 = Helper.clean_level(level_02)
        level_03 = Helper.clean_level(level_03)
        level_04 = Helper.clean_level(level_04)
        level_05 = Helper.clean_level(level_05)
        level_06 = Helper.clean_level(level_06)
        level_07 = Helper.clean_level(level_07)
        level_08 = Helper.clean_level(level_08)

        database.store_level_prototype(level_01)
        database.store_level_prototype(level_02)
        database.store_level_prototype(level_03)
        database.store_level_prototype(level_04)
        database.store_level_prototype(level_05)
        database.store_level_prototype(level_06)
        database.store_level_prototype(level_07)
        database.store_level_prototype(level_08)

        level_01 = evolution.evolve(80, level_01)
        level_02 = evolution.evolve(80, level_02)
        level_03 = evolution.evolve(80, level_03)
        level_04 = evolution.evolve(80, level_04)
        level_05 = evolution.evolve(80, level_05)
        level_06 = evolution.evolve(80, level_06)
        level_07 = evolution.evolve(80, level_07)
        level_08 = evolution.evolve(80, level_08)

        database.store_initial_level(level_01)
        database.store_initial_level(level_02)
        database.store_initial_level(level_03)
        database.store_initial_level(level_04)
        database.store_initial_level(level_05)
        database.store_initial_level(level_06)
        database.store_initial_level(level_07)
        database.store_initial_level(level_08)

if __name__ == "__main__":

    LevelSetup().initialize_levels()