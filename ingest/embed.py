import os
import chromadb
from sentence_transformers import SentenceTransformer
from chunk import chunk_corpus

# Resolves to portfolio-rag/chroma_db
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chroma_db"))

def embed_and_index():
    print("Loading embedding model (this may take a moment to download on the first run)...")
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    
    print(f"Connecting to ChromaDB at {DB_PATH}...")
    client = chromadb.PersistentClient(path=DB_PATH)
    
    # get_or_create_collection allows you to rerun this script safely without crashing
    collection = client.get_or_create_collection("portfolio")
    
    print("Loading chunks from the corpus...")
    chunks = chunk_corpus()
    if not chunks:
        print("No chunks found! Ensure you have markdown files in your corpus.")
        return
        
    texts = [c["text"] for c in chunks]
    
    print(f"Generating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(texts, normalize_embeddings=True).tolist()
    
    print("Adding vectors to ChromaDB...")
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        embeddings=embeddings,
        documents=texts,
        metadatas=[{"source": c["source"]} for c in chunks],
    )
    
    print(f"Success! Indexed {len(chunks)} chunks into ChromaDB.")

if __name__ == "__main__":
    embed_and_index()