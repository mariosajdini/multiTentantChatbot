from backend.app.db.database_connection import DatabaseConnection


class Collection:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_collection(self, collection_name, vector_params):
        self.db_connection.connect()
        self.db_connection.connection.create_collection(collection_name, vector_params)
        self.db_connection.close()

    def delete_collection(self, collection_name):
        self.db_connection.connect()
        self.db_connection.connection.delete_collection(collection_name)
        self.db_connection.close()

    def list_collections(self):
        self.db_connection.connect()
        collections = self.db_connection.connection.get_collections()
        self.db_connection.close()
        return collections
