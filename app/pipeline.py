import pandas as pd
from src.claims import extract_claims
from src.retrieval import retrieve_evidence
from src.llm_reasoner import llm_judge_claim


def run_pipeline(csv_path):
    df = pd.read_csv(csv_path)
    results = []

    for _, row in df.iterrows():
        example_id = row["id"]
        book_name = row["book_name"]
        backstory = row["content"]

        claims = extract_claims(backstory)

        claim_results = []
        final_label = "consistent"

        for claim in claims:
            evidence_chunks = retrieve_evidence(book_name, claim)
            llm_result = llm_judge_claim(claim, evidence_chunks)

            claim_results.append({
                "claim": claim,
                "verdict": llm_result["verdict"],
                "rationale": llm_result["rationale"],
                "evidence": evidence_chunks[0][:300]
            })

            if llm_result["verdict"] == "contradict":
                final_label = "contradict"

        results.append({
            "id": example_id,
            "prediction": final_label,
            "details": claim_results
        })

    return results
