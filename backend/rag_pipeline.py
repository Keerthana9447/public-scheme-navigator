# rag_pipeline.py
import json
import pickle
from .utils.embedder import Embedder
from .utils.retriever import Retriever


class RAGPipeline:
    def __init__(self):
        self.embedder = Embedder()
        self.retriever = Retriever()

    def load_schemes(self, path="backend/db/schemes.json"):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def retrieve_context(self, query: str):
        query_vec = self.embedder.embed_text(query)
        docs = self.retriever.search(query_vec)
        return docs

    def generate_answer(self, query: str, age: int = None, income: int = None):
        if age is not None and income is not None:
            schemes = self.load_schemes()
            eligible = [
                s["name"] for s in schemes
                if age >= s.get("min_age", 0)
                and age <= s.get("max_age", 200)
                and income <= s.get("income_limit", 999999)
            ]
            if eligible:
                return "✅ You are eligible for some services."
            else:
                return "❌ You are not eligible for any services."

        # fallback if no age/income provided
        context_docs = self.retrieve_context(query)
        if not context_docs:
            return "I couldn't find relevant schemes. Try asking about healthcare, education, or pensions."
        return f"I found schemes related to '{query}'. Please provide your age and income to check eligibility."
