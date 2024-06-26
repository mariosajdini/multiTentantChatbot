from backend.app.db.database_connection import DatabaseConnection
from qdrant_client import models


class Collection:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_collection(self, collection_name, vector_params):
        self.db_connection.connect()
        self.db_connection.connection.create_collection(collection_name, vector_params,
                                                        hnsw_config=models.HnswConfigDiff(
                                                            payload_m=16,
                                                            m=0,
                                                        ), )

    def delete_collection(self, collection_name):
        self.db_connection.connect()
        self.db_connection.connection.delete_collection(collection_name)

    def list_collections(self):
        self.db_connection.connect()
        collections = self.db_connection.connection.get_collections()
        return collections

    def get_collection(self, collection_name):
        self.db_connection.connect()
        collection = self.db_connection.connection.get_collection(collection_name)
        return collection
