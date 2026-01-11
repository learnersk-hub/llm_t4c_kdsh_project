import pandas as pd

df = pd.read_csv("data/train.csv")

print("Columns:")
print(df.columns)

print("\nFirst 5 rows:")
print(df.head())
