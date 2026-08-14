import os
import chromadb
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chroma_db"))

print("Initializing Hybrid Search models...")
embed_model = SentenceTransformer("BAAI/bge-small-en-v1.5", device="cpu")
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection("portfolio")

# Build the BM25 keyword index at startup
all_docs = collection.get()
corpus_texts = all_docs["documents"]
corpus_ids = all_docs["ids"]
tokenized_corpus = [doc.lower().split() for doc in corpus_texts]
bm25 = BM25Okapi(tokenized_corpus)

def reciprocal_rank_fusion(rankings, k=60):
    scores = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def hybrid_search(query: str, top_k: int = 20):
    # 1. Dense (Vector) Search
    query_embedding = embed_model.encode([query], normalize_embeddings=True).tolist()
    dense_results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    dense_ranking = dense_results["ids"][0]

    # 2. Sparse (BM25 Keyword) Search
    bm25_scores = bm25.get_scores(query.lower().split())
    bm25_ranking = [corpus_ids[i] for i in bm25_scores.argsort()[::-1][:top_k]]

    # 3. Fuse the rankings using RRF
    fused = reciprocal_rank_fusion([dense_ranking, bm25_ranking])
    top_ids = [doc_id for doc_id, _ in fused[:top_k]]

    # 4. Map IDs back to their actual text chunks
    id_to_text = dict(zip(corpus_ids, corpus_texts))
    return [{"id": i, "text": id_to_text[i]} for i in top_ids]

if __name__ == "__main__":
    # A quick test to verify it works
    res = hybrid_search("What AI tools are used?", top_k=2)
    print("\n--- Test Retrieval ---")
    print(res[0]["text"])