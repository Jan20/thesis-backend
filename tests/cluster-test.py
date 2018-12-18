import sys

sys.path.append("..")

from computations.cluster import Cluster
from database.database import Database


class ClusterTest(object):

    def compute_average_user_performance(self):

        Cluster().cluster_users()


if __name__ == "__main__":

    ClusterTest().compute_average_user_performance()
    
    print("Everything passed")
