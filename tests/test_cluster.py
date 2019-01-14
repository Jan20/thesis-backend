import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.set_up import set_up
from tests.set_up import clean_up
from cluster.cluster import Cluster
from database.database import Database
from normalization.normalization import Normalization

class Test_Cluster(object):

    def compute_average_user_performance(self):

        set_up()

        normalization: Normalization = Normalization()
        user_keys: str = Database().get_user_keys()

        for user_key in user_keys:

            normalization.calculate_average_performance(user_key)

        Cluster(1).cluster_users()
        clean_up()


if __name__ == "__main__":

    Test_Cluster().compute_average_user_performance()