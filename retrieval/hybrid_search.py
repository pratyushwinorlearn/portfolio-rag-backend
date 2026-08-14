import os
import re
from rank_bm25 import BM25Okapi

CORPUS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../corpus"))

def tokenize(text: str):
    # Extracts clean words only, stripping out question marks, periods, and punctuation
    return re.findall(r'\w+', text.lower())

def load_chunks():
    chunks = []
    print(f"Looking for corpus files in: {CORPUS_DIR}")
    if os.path.exists(CORPUS_DIR):
        for filename in os.listdir(CORPUS_DIR):
            if filename.endswith(".md"):
                filepath = os.path.join(CORPUS_DIR, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    sections = content.split("\n## ")
                    for sec in sections:
                        if sec.strip():
                            chunks.append(sec.strip())
    
    print(f"Successfully loaded {len(chunks)} chunks from corpus.")
    if not chunks:
        chunks = ["Pratyush is a B.Tech Computer Science student at Bennett University skilled in full-stack development and AI."]
    return chunks

_chunks = load_chunks()
_tokenized = [tokenize(doc) for doc in _chunks]
_bm25 = BM25Okapi(_tokenized)

def hybrid_search(query: str, top_k: int = 5):
    tokenized_query = tokenize(query)
    if not tokenized_query:
        return [{"text": _chunks[0]}]
        
    scores = _bm25.get_scores(tokenized_query)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    
    candidates = [{"text": _chunks[idx]} for idx in top_indices]
    return candidates