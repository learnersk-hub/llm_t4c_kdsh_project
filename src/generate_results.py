import pandas as pd
import numpy as np
import os

from sentence_transformers import SentenceTransformer
from src.clean_text import clean_gutenberg_text
from src.chunking import chunk_text
from src.claims import extract_claims


# ---------------- SETUP ---------------- #

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
    evidence_text = " ".join(evidence_chunks).lower()
    claim_words = claim.lower().split()

    # very conservative logic
    if "never" in evidence_text:
        return "contradict"

    if any(word in evidence_text for word in claim_words):
        return "support"

    return "neutral"


def final_label(verdicts):
    if verdicts.count("contradict") >= 2:
        return "contradict"
    return "consistent"


# ---------------- MAIN PIPELINE ---------------- #

def generate_results():
    test_df = pd.read_csv("data/train.csv")  # replace with test.csv for real test
    results = []

    # cache books (speed)
    book_cache = {}

    for _, row in test_df.iterrows():
        example_id = row["id"]
        book_name = row["book_name"]
        backstory = row["content"]

        # load book only once
        if book_name not in book_cache:
            chunks, embeddings = build_story_index(book_name)
            book_cache[book_name] = (chunks, embeddings)
        else:
            chunks, embeddings = book_cache[book_name]

        claims = extract_claims(backstory)
        verdicts = []

        for claim in claims:
            evidence = retrieve_evidence(claim, chunks, embeddings)
            verdict = judge_claim(claim, evidence)
            verdicts.append(verdict)

        prediction = final_label(verdicts)

        results.append({
            "id": example_id,
            "prediction": prediction
        })

        print(f"Processed ID {example_id} → {prediction}")

    # save CSV
    os.makedirs("results", exist_ok=True)
    results_df = pd.DataFrame(results)
    results_df.to_csv("results/results.csv", index=False)

    print("\n✅ results/results.csv GENERATED SUCCESSFULLY")


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    generate_results()
