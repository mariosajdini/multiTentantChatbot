from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.app.loaders.DocumentLoader import DocumentLoader
from backend.app.chatbot.chatbot import ChatBot
from backend.app.collection.Collection import Collection
from backend.app.db.database_connection import DatabaseConnection
from backend.app.db.vector_configuration import VectorConfiguration
from backend.app.services.embedding import EmbeddingService
import shutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost:5173",  # React frontend origin
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoint to load a document
@app.post("/load-document/")
async def load_document(file: UploadFile = File(...), tenant_id: str = Form(...)):
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    connection = DatabaseConnection()
    embedding_service = EmbeddingService(model=None, embedding_service="openai",
                                         qdrant_client=connection.connection)
    loader = DocumentLoader(file_path)
    documents = loader.load()
    embedding_service.embed_and_store_documents(documents, tenant_id=tenant_id)

    if documents is None:
        raise HTTPException(status_code=500, detail="Failed to load document")

    # Assuming the first document content is required for response
    return {"message": "Document loaded successfully", "content": documents[0]}


# Endpoint to start a chat
@app.post("/start-chat/")
async def start_chat(tenant_id: str = Form(...), question: str = Form(...)):
    try:
        collection_name = "test_collection"
        model_vendor = 'openai'
        model_name = 'gpt-4'
        chatBot = ChatBot(tenant_id, collection_name, model_vendor, model_name)
        reply = chatBot.chat(question).get("answer")

        if reply is None:
            raise HTTPException(status_code=500, detail="Chatbot failed to generate a response")

        return JSONResponse(content={"answer": reply})

    except Exception as e:
        logger.error(f"Error in start_chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
