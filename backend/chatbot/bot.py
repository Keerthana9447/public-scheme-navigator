
from ..rag_pipeline import RAGPipeline

class ChatBot:
    def __init__(self, rag: RAGPipeline):
        self.rag = rag

    def answer(self, query: str):
        return self.rag.generate_answer(query)
