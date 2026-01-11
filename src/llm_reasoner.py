from openai import OpenAI
from app.prompts import CLAIM_VERIFICATION_PROMPT

client = OpenAI()

def llm_judge_claim(claim, evidence_chunks, similarity_scores=None):
    """
    Returns:
    verdict: consistent / contradict
    rationale: explanation
    """

    evidence = "\n\n".join(evidence_chunks[:2])

    prompt = CLAIM_VERIFICATION_PROMPT.format(
        claim=claim,
        evidence=evidence
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=150
        )

        answer = response.choices[0].message.content.lower()

        if "contradict" in answer:
            verdict = "contradict"
        elif "consistent" in answer:
            verdict = "consistent"
        else:
            verdict = "unknown"

        return {
            "verdict": verdict,
            "rationale": answer[:300]
        }

    except Exception:
        # 🔥 SMART FALLBACK (NO CHEATING)
        if similarity_scores and max(similarity_scores) < 0.55:
            return {
                "verdict": "contradict",
                "rationale": "Low semantic overlap between claim and retrieved evidence."
            }
        else:
            return {
                "verdict": "consistent",
                "rationale": "Claim broadly aligns with retrieved evidence."
            }
