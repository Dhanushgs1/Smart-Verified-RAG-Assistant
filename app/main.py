from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Smart Verified RAG Assistant", version="1.0.0")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to Smart Verified RAG Assistant"}