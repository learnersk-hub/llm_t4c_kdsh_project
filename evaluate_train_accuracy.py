import pandas as pd
from app.pipeline import run_pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. Load ground truth
train_df = pd.read_csv("data/train.csv")

# 2. Run your model on training data
predictions = run_pipeline("data/train.csv")
pred_df = pd.DataFrame(predictions)

# 3. Merge predictions with true labels
merged = train_df.merge(pred_df, on="id")

# 4. Compute accuracy
acc = accuracy_score(merged["label"], merged["prediction"])

print("✅ Training Accuracy:", acc)

# Optional: deeper analysis
print("\nConfusion Matrix:")
print(confusion_matrix(merged["label"], merged["prediction"]))

print("\nClassification Report:")
print(classification_report(merged["label"], merged["prediction"]))
