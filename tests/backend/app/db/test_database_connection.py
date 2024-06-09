import unittest
from backend.app.db.database_connection import DatabaseConnection


class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        self.db_connection = DatabaseConnection()

    def test_connect(self):
        self.db_connection.connect()
        self.assertIsNotNone(self.db_connection.connection)


if __name__ == '__main__':
    unittest.main()
