from qdrant_client import QdrantClient
from backend.app.config import config

class DatabaseConnection:
    def __init__(self, path_to_db=None):
        self.host = config.QDRANT_HOST
        self.connection = None
        self.path_to_db = path_to_db

    def connect(self):
        self.connection = QdrantClient(self.host, port=6333)

    def close(self):
        self.connection.close()
