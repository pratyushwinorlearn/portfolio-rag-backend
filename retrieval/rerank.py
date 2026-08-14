from sentence_transformers import CrossEncoder

_reranker = None

def get_reranker():
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")
    return _reranker

def rerank(query: str, candidates: list, top_n: int = 5):
    reranker_model = get_reranker()
    pairs = [(query, c["text"]) for c in candidates]
    scores = reranker_model.predict(pairs)
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [c for c, _ in ranked[:top_n]]