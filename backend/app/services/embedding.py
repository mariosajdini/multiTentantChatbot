import os
import uuid
from langchain_openai import OpenAIEmbeddings
from qdrant_client.models import PointStruct
from langchain_qdrant import Qdrant


os.getenv('OPENAI_API_KEY')


def add_tenant_id_to_documents(documents, tenant_id):
    for document in documents:
        document.metadata['tenant_id'] = tenant_id


class EmbeddingService:
    def __init__(self, embedding_service, qdrant_client, model=None,collection_name=None):
        self.collection_name = collection_name
        self.qdrant_client = qdrant_client
        self.model = model
        self.embedding_service = embedding_service
        self.embedding_client = self.get_embedding_client()

    def embed_documents(self, documents):
        embeddings = self.embedding_client.embed_documents(documents)
        return embeddings

    def embed_and_store_documents(self, documents, tenant_id):
        doc_store = Qdrant.from_existing_collection(
            embedding=self.embedding_client,
            collection_name="test_collection",
            url="localhost:6333"
        )
        add_tenant_id_to_documents(documents, tenant_id)
        doc_store.add_documents(documents)

    def store_embedding(self, embeddings, docs, collection_name, tenant_id):
        points = []
        for i, document in enumerate(docs):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embeddings[i],
                payload={"page_content": document, "tenant_id": tenant_id}
            )
            points.append(point)
        self.qdrant_client.upsert(collection_name=collection_name, points=points)

    def get_embedding_client(self):
        if self.embedding_service == "openai":
            if self.model:
                return OpenAIEmbeddings(model=self.model)
            else:
                return OpenAIEmbeddings()
