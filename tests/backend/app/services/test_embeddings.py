import unittest

from backend.app.collection.Collection import Collection
from backend.app.db.database_connection import DatabaseConnection
from backend.app.db.vector_configuration import VectorConfiguration
from backend.app.services.embedding import EmbeddingService


class TestEmbeddingService(unittest.TestCase):
    def setUp(self):
        self.collection_name = 'test_collection'
        self.connection = DatabaseConnection()
        self.collection = Collection(db_connection=self.connection)
        self.VectorConfiguration = VectorConfiguration(vector_size=3, distance_metric='cosine')
        self.collection.create_collection(self.collection_name, self.VectorConfiguration.vector_params)
        self.embedding_service = EmbeddingService(model=None, embedding_service="openai",
                                                  qdrant_client=self.connection.connection)

    def tearDown(self):
        self.collection.delete_collection(self.collection_name)

    def test_embed_documents(self):
        documents = [
            "Hi there!",
            "Oh, hello!",
            "What's your name?",
            "My friends call me World",
            "Hello World!"
        ]
        embeddings = self.embedding_service.embed_documents(documents)
        self.assertEqual(len(embeddings), len(documents))
        self.assertIsNotNone(embeddings[0])

    def test_store_embedding(self):
        tenant_id = "test_tenant"
        embeddings = [
            [0.1, 0.2, 0.3],
            [0.2, 0.3, 0.4],
            [0.3, 0.4, 0.5],
            [0.4, 0.5, 0.6],
            [0.5, 0.6, 0.7]
        ]
        docs = [
            "Hi there!",
            "Oh, hello!",
            "What's your name?",
            "My friends call me World",
            "Hello World!"
        ]

        self.embedding_service.store_embedding(embeddings, docs, self.collection_name, tenant_id)


if __name__ == '__main__':
    unittest.main()
