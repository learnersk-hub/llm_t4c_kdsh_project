CLAIM_VERIFICATION_PROMPT = """
You are verifying a fictional character backstory against a novel.

CLAIM:
{claim}

EVIDENCE FROM NOVEL:
{evidence}

Question:
Does the evidence SUPPORT the claim, CONTRADICT it, or NOT MENTION it?

Answer with exactly one word:
support / contradict / neutral
"""
