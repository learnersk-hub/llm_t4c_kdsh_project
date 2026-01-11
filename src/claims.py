import pandas as pd

def extract_claims(backstory_text, max_claims=5):
    """
    Simple baseline claim extraction:
    - Split backstory into sentences
    - Take first few meaningful sentences as claims
    """
    text = backstory_text.replace("\n", " ")
    sentences = text.split(".")

    claims = []
    for s in sentences:
        s = s.strip()
        if len(s) > 20:
            claims.append(s)

        if len(claims) >= max_claims:
            break

    return claims


# -------- TEST -------- #

df = pd.read_csv("data/train.csv")
row = df.iloc[0]

backstory = row["content"]
character = row["char"]

claims = extract_claims(backstory)

print("Character:", character)
print("\nExtracted Claims:\n")
for i, claim in enumerate(claims, 1):
    print(f"{i}. {claim}")
