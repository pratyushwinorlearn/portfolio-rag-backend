def rerank(query: str, candidates: list, top_n: int = 5):
    return candidates[:top_n]