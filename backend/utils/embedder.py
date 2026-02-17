
import numpy as np
from .preprocess import clean_text

class Embedder:
    def embed_text(self, text: str):
        """Dummy embedding: convert chars to numbers"""
        text = clean_text(text)
        vec = np.array([ord(c) % 50 for c in text])  # simple numeric encoding
        return vec
