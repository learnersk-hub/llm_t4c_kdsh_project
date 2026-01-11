import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from src.clean_text import clean_gutenberg_text
from src.chunking import chunk_text
import os

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def build_story_index(book_name):
    book_file = os.path.join("books", f"{book_name}.txt")

    with open(book_file, "r", encoding="utf-8", errors="ignore") as f:
        raw_text = f.read()

    clean_text = clean_gutenberg_text(raw_text)
    chunks = chunk_text(clean_text)
    embeddings = model.encode(chunks)

    return chunks, embeddings


def retrieve_evidence(claim, chunks, embeddings, top_k=5):
    claim_embedding = model.encode([claim])[0]
    scores = np.dot(embeddings, claim_embedding)
    top_idx = np.argsort(scores)[-top_k:][::-1]

    return [chunks[i] for i in top_idx]


def judge_claim(claim, evidence_chunks):
    """
    Simple heuristic reasoning:
    - If evidence clearly mentions claim concepts → support
    - If evidence negates claim concepts → contradict
    - Else → neutral
    """

    evidence_text = " ".join(evidence_chunks).lower()
    claim_text = claim.lower()

    # Very simple keyword-based contradiction check (baseline)
    if "never" in evidence_text and any(word in evidence_text for word in claim_text.split()):
        return "contradict"

    if any(word in evidence_text for word in claim_text.split()):
        return "support"

    return "neutral"


# -------- TEST PIPELINE -------- #

df = pd.read_csv("data/train.csv")
row = df.iloc[0]

book_name = row["book_name"]
character = row["char"]
backstory = row["content"]

claims = backstory.replace("\n", " ").split(".")[:2]
claims = [c.strip() for c in claims if len(c.strip()) > 20]

print("Character:", character)
print("\nClaims:\n", claims)

chunks, embeddings = build_story_index(book_name)

print("\nReasoning Results:\n")

for claim in claims:
    evidence = retrieve_evidence(claim, chunks, embeddings)
    verdict = judge_claim(claim, evidence)

    print("CLAIM:", claim)
    print("VERDICT:", verdict)
    print("EVIDENCE (snippet):", evidence[0][:200])
    print("-" * 60)
