import numpy as np

class Retriever:
    def __init__(self, store_path="backend/db/vector_store.pkl"):
        import pickle
        try:
            with open(store_path, "rb") as f:
                self.vector_store = pickle.load(f)
        except Exception:
            self.vector_store = []

    def search(self, query_vec, top_k=3):
        if not self.vector_store:
            return ["No schemes available in vector store."]
        
        results = []
        for doc, vec in self.vector_store:
            try:
                sim = np.dot(query_vec, vec) / (np.linalg.norm(query_vec) * np.linalg.norm(vec))
            except Exception:
                sim = 0
            results.append((doc, sim))
        results.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in results[:top_k]]
