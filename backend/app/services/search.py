from qdrant_client import QdrantClient, models
from backend.app.db.database_connection import DatabaseConnection


class SearchService:
    def __init__(self):
        self.connection = DatabaseConnection()
        self.connection.connect()
        self.client = self.connection.connection

    def search(self, collection_name, tenant_id, query_vector, limit):
        query_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="tenant_id",
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
