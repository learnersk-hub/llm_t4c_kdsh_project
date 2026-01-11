import pathway as pw
from src.llm_reasoner import llm_judge_claim

@pw.udf
def llm_reason(claim, evidence):
    return llm_judge_claim(claim, evidence)
