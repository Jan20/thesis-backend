import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from computations.cluster import Cluster
from database.database import Database


class Test_Cluster(object):

    def compute_average_user_performance(self):

        Cluster().cluster_users()


if __name__ == "__main__":

    Test_Cluster().compute_average_user_performance()
    
    print("Everything passed")
