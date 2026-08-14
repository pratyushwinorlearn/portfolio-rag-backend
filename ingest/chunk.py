import re
import json
import os
from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

HEADERS_TO_SPLIT = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
]

def protect_code_blocks(text: str):
    blocks = re.findall(r"```[\s\S]*?```", text)
    for i, block in enumerate(blocks):
        text = text.replace(block, f"__CODEBLOCK_{i}__", 1)
    return text, blocks

def restore_code_blocks(text: str, blocks: list):
    for i, block in enumerate(blocks):
        text = text.replace(f"__CODEBLOCK_{i}__", block)
    return text

def chunk_file(path: Path):
    raw_text = path.read_text(encoding="utf-8")
    protected_text, code_blocks = protect_code_blocks(raw_text)

    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT)
    header_docs = header_splitter.split_text(protected_text)

    sub_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
    final_chunks = []

    for doc in header_docs:
        restored = restore_code_blocks(doc.page_content, code_blocks)
        for piece in sub_splitter.split_text(restored):
            if piece.strip():
                final_chunks.append({
                    "text": piece.strip(),
                    "source": path.stem,
                    "headers": doc.metadata
                })

    return final_chunks

def chunk_corpus(corpus_dir=None):
    if corpus_dir is None:
        corpus_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "corpus"))
    
    all_chunks = []
    corpus_path = Path(corpus_dir)

    if not corpus_path.exists():
        print(f"Directory '{corpus_dir}' does not exist!")
        return []

    for path in corpus_path.glob("*.md"):
        all_chunks.extend(chunk_file(path))

    return all_chunks

if __name__ == "__main__":
    chunks = chunk_corpus()
    print(f"Generated {len(chunks)} chunks across all project files.")
    if chunks:
        print("\n--- Sample Chunk ---")
        print(json.dumps(chunks[0], indent=2))