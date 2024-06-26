from qdrant_client import QdrantClient, models
from langchain_qdrant import Qdrant
from backend.app.db.database_connection import DatabaseConnection
from backend.app.services.embedding import EmbeddingService


class SearchService:
    def __init__(self):
        self.connection = DatabaseConnection()
        self.connection.connect()
        self.client = self.connection.connection
        self.embedding_service = EmbeddingService(model=None, embedding_service="openai",
                                                  qdrant_client=self.client).embedding_client

    def search(self, collection_name, tenant_id, query_vector, limit):
        query_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="metadata.tenant_id",
                    match=models.MatchValue(
                        value=tenant_id,
                    ),
                )
            ]
        )
        return self.client.search(
            collection_name=collection_name,
            query_filter=query_filter,
            query_vector=query_vector,
            limit=limit,
        )

    def get_tenant_retriever(self, collection_name, tenant_id, score_threshold=0.5, limit=2):
        qdrant = Qdrant(self.client, collection_name, self.embedding_service)
        filter = models.Filter(
            must=[

                models.FieldCondition(
                    key="metadata.tenant_id",
                    match=models.MatchValue(value=tenant_id)
                )
            ]
        )
        retriever = qdrant.as_retriever(
            search_kwargs={'filter': filter, "k": limit, "score_threshold": score_threshold})
        return retriever

    def query(self, retriever, query):
        return retriever.invoke(query)
