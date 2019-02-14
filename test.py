import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database

os.system('python tests/test_database.py')
os.system('python tests/test_normalization.py')
os.system('python tests/test_helper.py')
os.system('python tests/test_normalization.py')
os.system('python tests/test_performance.py')
os.system('python tests/test_session.py')
os.system('python tests/test_evolution.py')

