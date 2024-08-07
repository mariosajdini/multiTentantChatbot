import unittest

from qdrant_client import models

from backend.app.collection.Collection import Collection
from backend.app.db.database_connection import DatabaseConnection
from backend.app.db.vector_configuration import VectorConfiguration


class TestCollection(unittest.TestCase):
    def setUp(self):
        self.collection_name = 'test_collection'
        self.connection = DatabaseConnection()
        self.collection = Collection(db_connection=self.connection)
        self.VectorConfiguration = VectorConfiguration(vector_size=1536, distance_metric='cosine')

    def tearDown(self):
        self.collection.delete_collection(self.collection_name)

    def test_create_collection(self):
        self.collection.create_collection(self.collection_name, self.VectorConfiguration.vector_params)
        self.connection.connection.create_payload_index(
            collection_name=self.collection_name,
            field_name="metadata.tenant_id",
            field_schema=models.PayloadSchemaType.KEYWORD,
        )
        collections_response = self.collection.list_collections()
        collection_names = [collection.name for collection in collections_response.collections]
        self.assertIn(self.collection_name, collection_names)
        self.assertEqual(len(collection_names), 1)


if __name__ == '__main__':
    unittest.main()
