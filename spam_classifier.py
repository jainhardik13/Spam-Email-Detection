import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import pickle

# =========================
# 1. LOAD DATASET
# =========================
data = pd.read_csv("updated_dataset_18_02_2026.csv")

# Check for missing values before processing
print(f"Total rows: {len(data)}")
print(f"Rows with missing labels: {data['label'].isna().sum()}")
print(f"Rows with missing text: {data['text'].isna().sum()}")

# Drop rows with missing labels or text
data = data.dropna(subset=["label", "text"])
print(f"Rows after removing missing values: {len(data)}")

# Ensure labels are numeric (0 = ham, 1 = spam)
data["label"] = data["label"].astype(int)

# Basic sanity checks
print("Label distribution:")
print(data["label"].value_counts())
print(data["label"].value_counts(normalize=True))
print("Empty texts:", (data["text"].str.strip() == "").sum())

# =========================
# 2. TRAIN–TEST SPLIT (STRATIFIED)
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    data["text"],
    data["label"],
    test_size=0.2,
    random_state=42,
    stratify=data["label"]
)

print("\nTrain labels:")
print(y_train.value_counts())
print("\nTest labels:")
print(y_test.value_counts())

# =========================
# 3. TF-IDF VECTORIZATION
# =========================
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    min_df=1,          # important for small spam datasets
    max_df=0.9
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# =========================
# 4. MODEL TRAINING
# =========================
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    C=0.5
)

model.fit(X_train_vec, y_train)

# =========================
# 5. STANDARD EVALUATION
# =========================
y_pred_default = model.predict(X_test_vec)

print("\n=== Default Threshold (0.5) ===")
print("Accuracy:", accuracy_score(y_test, y_pred_default) * 100)
print(classification_report(y_test, y_pred_default))

# =========================
# 6. PROBABILITY + CUSTOM THRESHOLD
# =========================
y_proba = model.predict_proba(X_test_vec)[:, 1]

print("\nSample spam probabilities:")
print(y_proba[:10])

# Custom threshold (better for spam detection)
THRESHOLD = 0.3
y_pred_custom = (y_proba >= THRESHOLD).astype(int)

print(f"\n=== Custom Threshold ({THRESHOLD}) ===")
print(classification_report(y_test, y_pred_custom))

# =========================
# 7. MANUAL SAMPLE CHECK
# =========================
print("\nSample predictions:\n")
for i in range(10):
    print("Text:", X_test.iloc[i][:100])
    print("Spam probability:", round(y_proba[i] * 100, 2), "%")
    print("Prediction:", "Spam" if y_pred_custom[i] == 1 else "Not Spam")
    print("-" * 50)

# =========================
# 8. SAVE MODEL & VECTORIZER
# =========================
pickle.dump(model, open("Model/spam_model1.pkl", "wb"))
pickle.dump(vectorizer, open("Model/vectorizer1.pkl", "wb"))

print("\nModel and vectorizer saved successfully.")
