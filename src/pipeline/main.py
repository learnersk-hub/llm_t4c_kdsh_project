import pathway as pw
from ingest import load_backstories
from retrieve import retrieve_chunks
from reason import llm_reason
from src.claims import extract_claims

@pw.udf
def extract_claims_udf(text):
    return extract_claims(text)

def main():
    data = load_backstories("data/test.csv")

    claims = data.select(
        id=data.id,
        book=data.book_name,
        claims=extract_claims_udf(data.content),
    )

    exploded = claims.flatten(claims=claims.claims)

    evidence = exploded.select(
        id=exploded.id,
        verdict=llm_reason(
            exploded.claims,
            retrieve_chunks(exploded.book, exploded.claims),
        )
    )

    pw.io.csv.write(
        evidence,
        "results/intermediate.csv"
    )

    pw.run()

if __name__ == "__main__":
    main()
