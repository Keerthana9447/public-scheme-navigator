import json
import pickle
from utils.embedder import Embedder

def build_vector_store(schemes_path="backend/db/schemes.json", store_path="backend/db/vector_store.pkl"):
    embedder = Embedder()
    vector_store = []

    # Load schemes
    with open(schemes_path, "r", encoding="utf-8") as f:
        schemes = json.load(f)

    # Create embeddings for each scheme description
    for scheme in schemes:
        text = f"{scheme['name']} age {scheme.get('min_age',0)}-{scheme.get('max_age',200)} income_limit {scheme.get('income_limit',999999)}"
        vec = embedder.embed_text(text)
        vector_store.append((text, vec))

    # Save to pickle
    with open(store_path, "wb") as f:
        pickle.dump(vector_store, f)

    print(f"✅ Vector store built with {len(vector_store)} entries at {store_path}")

if __name__ == "__main__":
    build_vector_store()
