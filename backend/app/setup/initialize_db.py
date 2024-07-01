# backend/app/setup/initialize_db.py

import os
import sys


from dotenv import load_dotenv
from qdrant_client import models
from backend.app.collection.Collection import Collection
from backend.app.db.database_connection import DatabaseConnection
from backend.app.db.vector_configuration import VectorConfiguration
from backend.app.config import config  # Import Config

def initialize_collection():
    collection_name = config.COLLECTION_NAME  # Use centralized config
    connection = DatabaseConnection()
    collection = Collection(db_connection=connection)
    vector_config = VectorConfiguration(vector_size=1536, distance_metric='cosine')
    
    # Create collection
    collection.create_collection(collection_name, vector_config.vector_params)
    connection.connection.create_payload_index(
        collection_name=collection_name,
        field_name="metadata.tenant_id",
        field_schema=models.PayloadSchemaType.KEYWORD,
    )

if __name__ == "__main__":
    initialize_collection()

