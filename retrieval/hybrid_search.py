from sentence_transformers import SentenceTransformer
import chromadb
import os

_embed_model = None
_collection = None

def get_embed_model():
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer("BAAI/bge-small-en-v1.5", device="cpu")
    return _embed_model

def get_collection():
    global _collection
    if _collection is None:
        db_path = os.path.join(os.path.dirname(__file__), "../chroma_db")
        client = chromadb.PersistentClient(path=db_path)
        _collection = client.get_collection("portfolio_chunks")
    return _collection

def hybrid_search(query: str, top_k: int = 20):
    model = get_embed_model()
    collection = get_collection()
    
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    # Format results to match your expected structure
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    
    candidates = []
    for doc, meta in zip(documents, metadatas):
        candidates.append({"text": doc, "metadata": meta})
        
    return candidates