from qdrant_client import QdrantClient


class DatabaseConnection:
    def __init__(self, path_to_db=None):
        self.connection = None
        self.path_to_db = path_to_db

    def connect(self):
        self.connection = QdrantClient(path=self.path_to_db)

    def close(self):
        self.connection.close()
