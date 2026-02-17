import pytest
from backend.rag_pipeline import RAGPipeline

def test_retrieve_context():
    rag = RAGPipeline()
    docs = rag.retrieve_context("healthcare")
    assert isinstance(docs, list)
