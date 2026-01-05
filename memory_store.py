# memory_store.py
from sentence_transformers import SentenceTransformer
import chromadb

# -----------------------------------
# 1. Load Embedding Model
# -----------------------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------------
# 2. Initialize Chroma with Persistence
# -----------------------------------
chroma_client = chromadb.PersistentClient(path="./db")
collection = chroma_client.get_or_create_collection("memory")

# -----------------------------------
# 3. Generate Embedding
# -----------------------------------
def get_embedding(text: str):
    return embedding_model.encode(text).tolist()

# -----------------------------------
# 4. Store a Memory
# -----------------------------------
def store_memory(text: str):
    data = collection.get()
    memory_id = str(len(data.get("ids", [])))

    collection.add(
        ids=[memory_id],
        documents=[text],
        embeddings=[get_embedding(text)]
    )

    print(f"✅ Stored memory: {text}")

# -----------------------------------
# 5. Search Memory
# -----------------------------------
def search_memory(query: str, k: int = 3):
    results = collection.query(
        query_embeddings=[get_embedding(query)],
        n_results=k
    )
    return results["documents"][0]


def get_all_memories():
    data = collection.get()
    return data["documents"] if data else []
