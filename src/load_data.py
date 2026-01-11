import pandas as pd
import os

# Load train CSV
df = pd.read_csv("data/train.csv")

# Pick one example (for testing)
row = df.iloc[0]

example_id = row["id"]
book_name = row["book_name"]
character = row["char"]
backstory = row["content"]
label = row["label"]

# Book file path
book_file = os.path.join("books", f"{book_name}.txt")

# Load novel
with open(book_file, "r", encoding="utf-8") as f:
    novel_text = f.read()

print("Example ID:", example_id)
print("Book:", book_name)
print("Character:", character)
print("Label:", label)

print("\nBackstory:\n", backstory[:300], "...")
print("\nNovel length (words):", len(novel_text.split()))
