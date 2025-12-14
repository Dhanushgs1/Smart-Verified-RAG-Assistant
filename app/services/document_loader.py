from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_core.documents import Document
import os

def load_document(file_path: str) -> list[Document]:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        loader = PyPDFLoader(file_path)
    elif ext == '.txt':
        loader = TextLoader(file_path)
    elif ext == '.csv':
        loader = CSVLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    return loader.load()