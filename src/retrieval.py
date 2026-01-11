import os
import numpy as np
from sentence_transformers import SentenceTransformer

from src.clean_text import clean_gutenberg_text
from src.chunking import chunk_text


# ---------------- MODEL ---------------- #

model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------- CACHE ---------------- #
# To avoid rebuilding index for same book again and again

BOOK_INDEX_CACHE = {}


# ---------------- INDEX BUILDER ---------------- #

def build_chunk_index(book_name):
    """
    Load a book, clean it, chunk it, and create embeddings
    """
    book_file = os.path.join("books", f"{book_name}.txt")

    with open(book_file, "r", encoding="utf-8", errors="ignore") as f:
        raw_text = f.read()

    clean_text = clean_gutenberg_text(raw_text)
    chunks = chunk_text(clean_text)

    embeddings = model.encode(chunks, show_progress_bar=True)

    return chunks, embeddings


# ---------------- RETRIEVAL API (USED BY PIPELINE) ---------------- #

def retrieve_evidence(book_name, claim, k=5):
    """
    Main retrieval function used by Pathway pipeline.
    Returns top-k relevant text chunks (only text, no scores).
    """

    # Build index once per book
    if book_name not in BOOK_INDEX_CACHE:
        print(f"Building index for book: {book_name}")
        chunks, embeddings = build_chunk_index(book_name)
        BOOK_INDEX_CACHE[book_name] = (chunks, embeddings)
    else:
        chunks, embeddings = BOOK_INDEX_CACHE[book_name]

    # Encode query
    query_embedding = model.encode([claim])[0]

    # Similarity search
    scores = np.dot(embeddings, query_embedding)
    top_indices = np.argsort(scores)[-k:][::-1]

    # Return only chunk text (LLM-friendly)
    return [chunks[i] for i in top_indices]
