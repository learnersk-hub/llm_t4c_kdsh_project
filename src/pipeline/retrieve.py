import pathway as pw
from src.chunking import chunk_text
from src.clean_text import clean_gutenberg_text
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

@pw.udf
def retrieve_chunks(book_name, claim):
    book_file = os.path.join("books", f"{book_name}.txt")
    text = open(book_file, encoding="utf-8").read()
    clean = clean_gutenberg_text(text)
    chunks = chunk_text(clean)

    embeddings = model.encode(chunks)
    query_emb = model.encode([claim])[0]

    scores = embeddings @ query_emb
    top = scores.argsort()[-3:][::-1]

    return [chunks[i] for i in top]
