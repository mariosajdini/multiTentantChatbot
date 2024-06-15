import unittest
from backend.app.chatbot.chatbot import ChatBot
from backend.app.collection.Collection import Collection
from backend.app.db.database_connection import DatabaseConnection
from backend.app.db.vector_configuration import VectorConfiguration
from backend.app.services.embedding import EmbeddingService


class TestChatBot(unittest.TestCase):
    def setUp(self):
        self.tenant_id = 'test_tenant_id'
        self.collection_name = 'test_collection'
        self.model_vendor = 'openai'
        self.model_name = 'gpt-4o'
        self.connection = DatabaseConnection()
        self.connection.connect()
        self.client = self.connection.connection
        self.collection = Collection(db_connection=self.connection)
        self.VectorConfiguration = VectorConfiguration(vector_size=1536, distance_metric='cosine')
        self.collection.create_collection(self.collection_name, self.VectorConfiguration.vector_params)
        self.embedding_service = EmbeddingService(embedding_service='openai', qdrant_client=self.client)
    def tearDown(self):
        self.collection.delete_collection(self.collection_name)

    def test_initialize_chatbot(self):
        chat = ChatBot(self.tenant_id, self.collection_name, self.model_vendor, self.model_name)
        chatbot = chat.chatbot
        self.assertIsNotNone(chatbot)

    def test_chat(self):
        chat = ChatBot(self.tenant_id, self.collection_name, self.model_vendor, self.model_name)
        question = 'What is the capital of France?'
        answer = chat.chat(question)
        self.assertIsNotNone(answer)

    def test_chat_with_documents(self):
        chat = ChatBot(self.tenant_id, self.collection_name, self.model_vendor, self.model_name)
        question = 'How old is Marios? and what is his dream?'
        documents = [
            'Marios is 21 years old and he is a student.',
            'His dream is to become a software engineer.'
        ]
        embeddings = self.embedding_service.embed_documents(documents)
        self.embedding_service.store_embedding(embeddings, documents, self.collection_name, self.tenant_id)
        answer = chat.chat(question)
        self.assertIsNotNone(answer)


