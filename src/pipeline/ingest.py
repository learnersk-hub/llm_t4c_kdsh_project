import pathway as pw

def load_backstories(csv_path):
    return pw.io.csv.read(
        csv_path,
        schema={
            "id": int,
            "book_name": str,
            "content": str,
        },
        mode="static"
    )
