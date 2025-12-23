import faiss
import numpy as np
import os
import pandas as pd

FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "data/faiss.index")

# Example: create/load FAISS index for supplier embeddings
def get_faiss_index(dim=4):
    if os.path.exists(FAISS_INDEX_PATH):
        index = faiss.read_index(FAISS_INDEX_PATH)
    else:
        index = faiss.IndexFlatL2(dim)
    return index

def save_faiss_index(index):
    faiss.write_index(index, FAISS_INDEX_PATH)

# Example: add supplier embeddings (mock)
def add_supplier_embeddings(df: pd.DataFrame, index):
    # For demo, use numeric columns as embeddings
    vectors = df[["reliability_score", "past_delivery_rate", "on_time_percentage"]].values.astype(np.float32)
    index.add(vectors)
    save_faiss_index(index)
