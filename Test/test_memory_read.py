# test_memory_read.py
import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load SAME persistent DB
chroma_client = chroma_db = chromadb.PersistentClient(path="./db")

collection = chroma_client.get_collection("memory")

print("\n📂 Stored Memory IDs:", collection.get()["ids"])
print("📄 Stored Memory Documents:", collection.get()["documents"])
