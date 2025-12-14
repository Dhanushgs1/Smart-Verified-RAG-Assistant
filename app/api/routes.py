from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.services.rag_pipeline import rag_pipeline
from app.services.document_loader import load_document
from app.services.chunker import chunk_text
from app.services.vector_store import create_vector_store
import os

router = APIRouter()

@router.post("/upload", response_model=dict)
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = f"data/raw/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        # Process file
        documents = load_document(file_path)
        chunks = chunk_text(documents)
        create_vector_store(chunks)
        return {"message": f"File {file.filename} uploaded and processed successfully"}
    except Exception as e:
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = rag_pipeline(request.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))