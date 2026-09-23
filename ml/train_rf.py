import os

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from imblearn.over_sampling import SMOTE

from ml.preprocessing import preprocess_dataframe


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "model_dataset.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "intrusion_model.pkl"
)

ENCODER_PATH = os.path.join(
    MODEL_DIR,
    "label_encoder.pkl"
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

def load_data():
    """Load the processed intrusion detection dataset."""

    print("Loading dataset...")

    df = pd.read_csv(DATA_PATH)

    print(f"Dataset shape: {df.shape}")

    X = preprocess_dataframe(
        df,
        include_label=False
    )

    y = df["Label"]

    return X, y


# --------------------------------------------------
# Encode labels
# --------------------------------------------------

def encode_labels(y):
    """Convert attack class names into numeric labels."""

    encoder = LabelEncoder()

    y_encoded = encoder.fit_transform(y)

    print("\nClass encoding:")

    for label, encoded in zip(
        encoder.classes_,
        encoder.transform(encoder.classes_)
    ):
        print(f"{label} -> {encoded}")

    return y_encoded, encoder


# --------------------------------------------------
# Split data
# --------------------------------------------------

def split_data(X, y):
    """Create a stratified train/test split."""

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("\nData split:")
    print(f"Training set: {X_train.shape}")
    print(f"Testing set:  {X_test.shape}")

    return X_train, X_test, y_train, y_test


# --------------------------------------------------
# Handle missing values
# --------------------------------------------------

def handle_missing_values(X_train, X_test):
    """
    Fill missing values using medians calculated
    from the training set only.
    """

    train_medians = X_train.median()

    X_train = X_train.fillna(train_medians)
    X_test = X_test.fillna(train_medians)

    print("\nMissing values:")
    print(
        f"Training NaNs: "
        f"{X_train.isna().sum().sum()}"
    )

    print(
        f"Testing NaNs: "
        f"{X_test.isna().sum().sum()}"
    )

    return X_train, X_test


# --------------------------------------------------
# SMOTE
# --------------------------------------------------

def apply_smote(X_train, y_train):
    """
    Apply targeted SMOTE to minority classes.

    Bot (1)          -> 8,500 samples
    Web Attack (6)   -> 8,500 samples
    """

    print("\nApplying SMOTE...")

    smote = SMOTE(
        sampling_strategy={
            1: 8500,
            6: 8500
        },
        random_state=42
    )

    X_train_smote, y_train_smote = smote.fit_resample(
        X_train,
        y_train
    )

    print(
        f"Before SMOTE: {X_train.shape}"
    )

    print(
        f"After SMOTE:  {X_train_smote.shape}"
    )

    print("\nClass distribution after SMOTE:")

    print(
        pd.Series(y_train_smote)
        .value_counts()
        .sort_index()
    )

    return X_train_smote, y_train_smote


# --------------------------------------------------
# Train Random Forest
# --------------------------------------------------

def train_random_forest(X_train, y_train):
    """Train the final tuned Random Forest."""

    print("\nTraining Random Forest...")

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=20,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train
    )

    print("Random Forest training complete.")

    return model


# --------------------------------------------------
# Save model
# --------------------------------------------------

def save_model(model, encoder):
    """Save trained model and label encoder."""

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    joblib.dump(
        encoder,
        ENCODER_PATH
    )

    print("\nModel saved to:")
    print(MODEL_PATH)

    print("\nLabel encoder saved to:")
    print(ENCODER_PATH)


# --------------------------------------------------
# Complete training pipeline
# --------------------------------------------------

def train():
    """Run the complete Random Forest training pipeline."""

    X, y = load_data()

    y_encoded, encoder = encode_labels(y)

    X_train, X_test, y_train, y_test = split_data(
        X,
        y_encoded
    )

    X_train, X_test = handle_missing_values(
        X_train,
        X_test
    )

    X_train_smote, y_train_smote = apply_smote(
        X_train,
        y_train
    )

    model = train_random_forest(
        X_train_smote,
        y_train_smote
    )

    save_model(
        model,
        encoder
    )

    return model, encoder, X_test, y_test


# --------------------------------------------------
# Run script
# --------------------------------------------------

if __name__ == "__main__":
    train()