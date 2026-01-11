import pandas as pd
import os
from src.clean_text import clean_gutenberg_text


def chunk_text(text, chunk_size=1000, overlap=200):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap

    return chunks


# -------- TEST PIPELINE -------- #

df = pd.read_csv("data/train.csv")
row = df.iloc[0]

book_name = row["book_name"]
book_file = os.path.join("books", f"{book_name}.txt")

with open(book_file, "r", encoding="utf-8", errors="ignore") as f:
    raw_text = f.read()

clean_text = clean_gutenberg_text(raw_text)
chunks = chunk_text(clean_text)

print("Book:", book_name)
print("Total words after cleaning:", len(clean_text.split()))
print("Total chunks:", len(chunks))

print("\nFirst chunk (300 chars):\n")
print(chunks[0][:300])
