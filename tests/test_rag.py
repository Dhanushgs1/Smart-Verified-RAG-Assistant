import pytest
from app.services.rag_pipeline import rag_pipeline

def test_rag_pipeline():
    # Test with no documents
    response = rag_pipeline("What is AI?")
    assert response.response == "No documents uploaded yet."
    assert response.sources == []