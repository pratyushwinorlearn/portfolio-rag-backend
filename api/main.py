import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel

# Ensure we can import from the retrieval folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retrieval.hybrid_search import hybrid_search
from retrieval.rerank import rerank
from api.prompts import SYSTEM_PROMPT

app = FastAPI()

# Allow your React frontend to communicate with this API
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# Toggle this to True later when deploying to production with Groq
USE_GROQ = os.getenv("USE_GROQ", "false").lower() == "true"

class ChatRequest(BaseModel):
    query: str

def build_prompt(query, contexts):
    # Only append context if we actually have some
    context_block = "\n\n".join(f"- {c['text']}" for c in contexts)
    return f"{SYSTEM_PROMPT}\n\nContext:\n{context_block}\n\nUser: {query}\nPortfolioOS AI:"

@app.post("/chat")
async def chat(req: ChatRequest):
    print(f"Received query: {req.query}")
    
    # 1. Retrieve candidates using dense + sparse search
    candidates = hybrid_search(req.query, top_k=20)
    
    # 2. Rerank the top candidates using the cross-encoder
    top_contexts = rerank(req.query, candidates, top_n=5)
    
    # 3. Inject the best contexts into the final LLM prompt
    prompt = build_prompt(req.query, top_contexts)

    async def event_stream():
        if USE_GROQ:
            from groq import Groq
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            stream = client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            for chunk in stream:
                token = chunk.choices[0].delta.content or ""
                yield {"data": token}
        else:
            import ollama
            # Streaming from the local Ollama instance on your RTX 4060
            stream = ollama.chat(
                model="qwen2.5:7b-instruct",
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            for chunk in stream:
                yield {"data": chunk["message"]["content"]}

    return EventSourceResponse(event_stream())