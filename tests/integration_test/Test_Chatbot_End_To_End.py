import unittest

from backend.app.chatbot.chatbot import ChatBot
from backend.app.collection.Collection import Collection
from backend.app.db.database_connection import DatabaseConnection
from backend.app.db.vector_configuration import VectorConfiguration
from backend.app.services.embedding import EmbeddingService
from backend.app.loaders.DocumentLoader import DocumentLoader


class TestChatBot(unittest.TestCase):
    def setUp(self):
        self.file_path = "data/ACM_BeckmanReport.pdf"
        self.loader = DocumentLoader(self.file_path)
        self.collection_name = 'test_collection'
        self.connection = DatabaseConnection()
        self.tenant_id = "test_tenant"
        self.model_vendor = 'openai'
        self.model_name = 'gpt-4o'
        self.collection = Collection(db_connection=self.connection)
        self.VectorConfiguration = VectorConfiguration(vector_size=1536, distance_metric='cosine')
        self.collection.create_collection(self.collection_name, self.VectorConfiguration.vector_params)
        self.embedding_service = EmbeddingService(model=None, embedding_service="openai",
                                                  qdrant_client=self.connection.connection)
        documents = self.loader.load()
        self.embedding_service.embed_and_store_documents(documents, self.tenant_id)

    def tearDown(self):
        self.collection.delete_collection(self.collection_name)

    def test_chatbot(self):
        chatBot = ChatBot(self.tenant_id, self.collection_name, self.model_vendor, self.model_name)
        reply = chatBot.chat("What is diversity in data management?").get("answer")
        self.assertIsNotNone(reply)

    def test_chatbot_with_multitenancy(self):
        tenant_2 = "test_tenant_2"
        tenant_2_file_path = "data/test.pdf"
        tenant_2_loader = DocumentLoader(tenant_2_file_path)
        tenant_2_documents = tenant_2_loader.load()
        self.embedding_service.embed_and_store_documents(tenant_2_documents, tenant_2)
        chatBot = ChatBot(tenant_2, self.collection_name, self.model_vendor, self.model_name)
        reply = chatBot.chat("What is diversity in data management?").get("answer")
        self.assertEqual(reply, "I don't know.")



