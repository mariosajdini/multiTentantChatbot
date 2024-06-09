import os
import uuid
from langchain_openai import OpenAIEmbeddings
from qdrant_client.models import PointStruct
from langchain_qdrant import Qdrant
from backend.app.db.database_connection import DatabaseConnection

os.getenv('OPENAI_API_KEY')


class EmbeddingService:
    def __init__(self, model, embedding_service, qdrant_client):
        self.qdrant_client = qdrant_client
        self.model = model
        self.embedding_service = embedding_service
        self.embedding_client = self.get_embedding_client()

    def embed_documents(self, documents):
        embeddings = self.embedding_client.embed_documents(documents)
        return embeddings

    def store_embedding(self, embeddings, docs, collection_name, tenant_id):
        points = []
        for i, document in enumerate(docs):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embeddings[i],
                payload={"document": document, "tenant_id": tenant_id}
            )
            points.append(point)
        self.qdrant_client.upsert(collection_name=collection_name, points=points)

    def get_embedding_client(self):
        if self.embedding_service == "openai":
            if self.model:
                return OpenAIEmbeddings(model=self.model)
            else:
                return OpenAIEmbeddings()
