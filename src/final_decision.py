import pandas as pd

def final_label(verdicts):
    """
    verdicts: list of 'support' / 'neutral' / 'contradict'
    """
    contradict_count = verdicts.count("contradict")

    # Conservative rule (judge-friendly)
    if contradict_count >= 2:
        return "contradict"
    else:
        return "consistent"


# -------- TEST WITH YOUR OUTPUT -------- #

verdicts = ["contradict", "contradict"]
label = final_label(verdicts)

print("Final decision:", label)
