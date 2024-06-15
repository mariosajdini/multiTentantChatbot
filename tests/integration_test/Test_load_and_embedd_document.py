import unittest

from backend.app.collection.Collection import Collection
from backend.app.db.database_connection import DatabaseConnection
from backend.app.db.vector_configuration import VectorConfiguration
from backend.app.services.embedding import EmbeddingService
from backend.app.loaders.DocumentLoader import DocumentLoader


class TestLoadAndEmbedDocument(unittest.TestCase):
    def setUp(self):
        self.file_path = "data/test.pdf"
        self.loader = DocumentLoader(self.file_path)
        self.collection_name = 'test_collection'
        self.connection = DatabaseConnection()
        self.collection = Collection(db_connection=self.connection)
        self.VectorConfiguration = VectorConfiguration(vector_size=1536, distance_metric='cosine')
        self.collection.create_collection(self.collection_name, self.VectorConfiguration.vector_params)
        self.embedding_service = EmbeddingService(model=None, embedding_service="openai",
                                                  qdrant_client=self.connection.connection)

    def tearDown(self):
        self.collection.delete_collection(self.collection_name)

    def test_load_and_embed_document(self):
        documents = self.loader.load()
        self.assertIsNotNone(documents)
        self.assertEqual(len(documents), 8)
        self.embedding_service.embed_and_store_documents(documents, tenant_id="test_tenant")
        collection_points = self.collection.get_collection(self.collection_name).points_count
        self.assertEqual(collection_points, 8)

