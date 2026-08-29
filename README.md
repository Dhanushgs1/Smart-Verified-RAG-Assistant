# Smart Verified RAG Assistant

A FastAPI service that answers questions strictly from documents you upload.
Retrieval is grounded in a FAISS index built from those files, and the prompt
instructs the model to refuse rather than guess when the answer is not in the
retrieved context.

## Stack

| Layer            | Choice                                  |
| ---------------- | --------------------------------------- |
| API              | FastAPI + Uvicorn                       |
| Orchestration    | LangChain (LCEL runnables)              |
| LLM              | OpenAI `gpt-3.5-turbo`                  |
| Vector store     | FAISS (`faiss-cpu`), persisted locally  |
| Parsing          | `pypdf`                                 |
| Tests            | Pytest                                  |
| Packaging        | Dockerfile (python:3.11-slim)           |

## Running it

```bash
python -m venv .venv
```

```bash
.venv/Scripts/activate
```

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-...
```

`app/core/config.py` loads it through `pydantic-settings`, and the key is
**required**: the app raises at import time if it is missing.

```bash
uvicorn app.main:app --reload
```

Swagger UI is at `http://127.0.0.1:8000/docs`.

The upload route writes to `data/raw/`, so create that directory before the
first upload:

```bash
mkdir -p data/raw
```

### Docker

```bash
docker build -t smart-verified-rag .
```

```bash
docker run -p 8000:8000 --env-file .env smart-verified-rag
```

## API

| Method | Route     | Body                       | Returns                              |
| ------ | --------- | -------------------------- | ------------------------------------ |
| GET    | `/`       | none                       | Health message.                      |
| POST   | `/upload` | `multipart/form-data` file | Confirmation once the file is chunked and indexed. |
| POST   | `/chat`   | `{ "message": "..." }`     | `{ "response": ..., "sources": [] }` |

If a file fails to process, the partially written upload is deleted and the
route returns a 500 with the underlying error rather than leaving a
half-indexed document behind.

## Pipeline

```
upload  ->  document_loader  ->  chunker  ->  embeddings  ->  FAISS store
                                                                  |
question  ------------------  retriever  --------------------------+
                                   |
                       RAG_PROMPT + ChatOpenAI  ->  answer
```

`app/services/rag_pipeline.py` builds the chain with LCEL. If no vector store
exists yet it short-circuits with "No documents uploaded yet." instead of
letting the model answer from its own training data.

## Layout

```
app/
  main.py                FastAPI app and router mount
  api/routes.py          /upload and /chat
  core/config.py         Settings from .env
  core/prompts.py        The grounding prompt
  models/chat.py         Request and response schemas
  services/
    document_loader.py   Read the uploaded file
    chunker.py           Split into chunks
    embeddings.py        Embedding model
    vector_store.py      Create / load the FAISS index
    rag_pipeline.py      Retrieval and generation chain
  utils/helpers.py
tests/test_rag.py
Dockerfile
```

## Known gaps

- `ChatResponse.sources` is always an empty list. Citation plumbing is not
  written yet, so answers cannot be traced back to a page.
- `rag_pipeline.process_uploaded_file()` calls `load_document`, `chunk_text`
  and `create_vector_store` without importing them. The live path in
  `api/routes.py` imports them properly, so that helper is dead code that
  would raise if it were ever called.
