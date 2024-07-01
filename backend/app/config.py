# backend/app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'default_collection')
    QDRANT_HOST = os.getenv('QDRANT_HOST', 'localhost')


config = Config()
