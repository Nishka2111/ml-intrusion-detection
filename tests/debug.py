import joblib
import numpy as np
import pandas as pd

MODEL_PATH = "models/intrusion_model.pkl"
ENCODER_PATH = "models/label_encoder.pkl"
DATASET_PATH = "data/processed/model_dataset.csv"

print("\n=== Loading artifacts ===")

model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

print("Model:", type(model).__name__)
print("Model classes:", model.classes_)
print("Number of features:", len(model.feature_names_in_))
print("Encoder classes:", encoder.classes_)

print("\n=== Loading dataset ===")

df = pd.read_csv(DATASET_PATH)

print("Dataset shape:", df.shape)
print("Columns:", len(df.columns))

# Separate target
if "Label" in df.columns:
    y = df["Label"]
    X = df.drop(columns=["Label"])
else:
    raise ValueError("Label column not found")

# Replace infinity
X = X.replace([np.inf, -np.inf], np.nan)

# Make sure we use exactly the model's expected features
expected_features = list(model.feature_names_in_)

missing = [c for c in expected_features if c not in X.columns]

print("Missing model features:", len(missing))

if missing:
    print("Missing columns:")
    for col in missing:
        print(" -", col)
    raise ValueError("Dataset does not contain all model features")

X = X[expected_features]

# Fill missing values
X = X.fillna(X.median(numeric_only=True))
X = X.fillna(0)

print("Final X shape:", X.shape)

print("\n=== Testing predictions ===")

# Take 1000 random rows
sample = X.sample(
    n=min(1000, len(X)),
    random_state=42
)

predictions = model.predict(sample)

print("Number of predictions:", len(predictions))

unique, counts = np.unique(predictions, return_counts=True)

print("\nRaw model prediction distribution:")

for label, count in zip(unique, counts):
    print(f"{label}: {count}")

print("\nDecoded prediction distribution:")

decoded = encoder.inverse_transform(predictions.astype(int))

decoded_unique, decoded_counts = np.unique(
    decoded,
    return_counts=True
)

for label, count in zip(decoded_unique, decoded_counts):
    print(f"{label}: {count}")

print("\n=== Testing first 20 rows ===")

first_20 = model.predict(X.iloc[:20])

decoded_20 = encoder.inverse_transform(
    first_20.astype(int)
)

for i, prediction in enumerate(decoded_20):
    print(f"Row {i}: {prediction}")

print("\n=== Probability check ===")

proba = model.predict_proba(X.iloc[:10])

for i, probabilities in enumerate(proba):
    top_index = np.argmax(probabilities)

    print(
        f"Row {i}: "
        f"class={encoder.inverse_transform([top_index])[0]}, "
        f"confidence={probabilities[top_index]:.4f}"
    )