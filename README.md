# Smart Verified RAG Assistant 🤖

A production-style **Retrieval-Augmented Generation (RAG)** system that answers
questions strictly from uploaded documents and prevents hallucinations.

## 🚀 Features
- Upload PDF documents
- Semantic search using embeddings
- FAISS vector database
- Strict no-hallucination responses
- FastAPI backend with Swagger UI
- Tested using Pytest

## 🛠 Tech Stack
- Python
- FastAPI
- LangChain
- FAISS
- OpenAI API
- Pytest

## ▶️ How to Run
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app
