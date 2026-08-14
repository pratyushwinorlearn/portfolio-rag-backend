import os
from rank_bm25 import BM25Okapi

# Load your markdown corpus files dynamically on startup
CORPUS_DIR = os.path.join(os.path.dirname(__file__), "../corpus")

def load_chunks():
    chunks = []
    if os.path.exists(CORPUS_DIR):
        for filename in os.listdir(CORPUS_DIR):
            if filename.endswith(".md"):
                filepath = os.path.join(CORPUS_DIR, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Split markdown by headers to create distinct chunks
                    sections = content.split("\n## ")
                    for sec in sections:
                        if sec.strip():
                            chunks.append(sec.strip())
    
    # Fallback if corpus folder isn't found
    if not chunks:
        chunks = ["Pratyush is a B.Tech Computer Science student at Bennett University skilled in full-stack development and AI."]
    return chunks

# Initialize BM25 index in memory (uses < 5MB RAM)
_chunks = load_chunks()
_tokenized = [doc.lower().split(" ") for doc in _chunks]
_bm25 = BM25Okapi(_tokenized)

def hybrid_search(query: str, top_k: int = 5):
    tokenized_query = query.lower().split(" ")
    scores = _bm25.get_scores(tokenized_query)
    
    # Get top matching chunk indices
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    
    candidates = []
    for idx in top_indices:
        candidates.append({"text": _chunks[idx]})
        
    return candidates