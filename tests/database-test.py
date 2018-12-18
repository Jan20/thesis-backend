import sys

sys.path.append("..")

from computations.transform import Transform
from database.database import Database


class DatabaseTest(object):

    #
    # Calculates the average performance for
    # every user stored at Firebase.
    #
    def compute_average_performance_for_every_user(self):

        #
        # 
        #
        database: Database = Database()
        transform: Transform = Transform()

        user_keys: [str] = database.get_user_keys()

        print(user_keys)

        for user_key in user_keys:
                
                
            transform.calculate_average_performance(user_key)

#
# Run
#
if __name__ == "__main__":

    DatabaseTest().compute_average_user_performance()