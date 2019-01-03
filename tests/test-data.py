from database.database import Database

class TestData:

    def __init__(self):

        database: Database = Database()

    def generate_test_data(self):

        self.database.get_highest_user_id()