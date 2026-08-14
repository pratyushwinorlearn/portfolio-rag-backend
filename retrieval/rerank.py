from sentence_transformers import CrossEncoder

_reranker = None

def get_reranker():
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")
    return _reranker

def rerank(query: str, candidates: list, top_n: int = 5):
    # BM25 already ranks them accurately; just return top N
    return candidates[:top_n]