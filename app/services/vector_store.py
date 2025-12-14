from langchain_community.vectorstores import FAISS
from app.services.embeddings import embeddings
import os

VECTOR_DB_PATH = "data/vectordb"

def create_vector_store(chunks: list):
    if os.path.exists(VECTOR_DB_PATH):
        vectorstore = FAISS.load_local(VECTOR_DB_PATH, embeddings)
        vectorstore.add_documents(chunks)
    else:
        vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTOR_DB_PATH)
    return vectorstore

def load_vector_store():
    index_path = os.path.join(VECTOR_DB_PATH, "index.faiss")
    if os.path.exists(index_path):
        return FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    return None