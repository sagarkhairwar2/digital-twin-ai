# test_memory_write.py
import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Chroma persistent client
chroma_client = chromadb.PersistentClient(path="./db")

collection = chroma_client.get_or_create_collection(
    name="memory"
)

def get_embedding(text):
    return embedding_model.encode(text).tolist()

def store_memory(text):
    emb = get_embedding(text)
    memory_id = str(len(collection.get()["ids"]))

    collection.add(
        ids=[memory_id],
        documents=[text],
        embeddings=[emb]
    )
    print("Stored:", text)

# ----- WRITE MEMORY -----
store_memory("This is a persistent memory test")
store_memory("My favorite color is red")
store_memory("I study at night")
