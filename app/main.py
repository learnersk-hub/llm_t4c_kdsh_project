import os
import pandas as pd
from app.pipeline import run_pipeline


def main():
    results = run_pipeline("data/test.csv")

    rows = []
    for r in results:
        for d in r["details"]:
            rows.append({
                "id": r["id"],
                "prediction": r["prediction"],
                "claim": d["claim"],
                "claim_verdict": d["verdict"],
                "rationale": d["rationale"],
                "evidence_snippet": d["evidence"]
            })

    os.makedirs("results", exist_ok=True)
    pd.DataFrame(rows).to_csv("results/results.csv", index=False)

    print("✅ results/results.csv generated with rationale")


if __name__ == "__main__":
    main()
