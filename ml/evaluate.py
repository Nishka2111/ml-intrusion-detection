import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support
)


def calculate_metrics(y_true, y_pred):
    """
    Calculate overall classification metrics.
    """

    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_precision": precision_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0
        ),
        "macro_recall": recall_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0
        ),
        "macro_f1": f1_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0
        )
    }


def get_classification_report(y_true, y_pred, class_names):
    """
    Generate a classification report.
    """

    return classification_report(
        y_true,
        y_pred,
        target_names=class_names,
        zero_division=0
    )


def get_confusion_matrix(y_true, y_pred):
    """
    Generate a confusion matrix.
    """

    return confusion_matrix(y_true, y_pred)


def get_class_metrics(y_true, y_pred, class_names):
    """
    Calculate metrics for each class.
    """

    precision, recall, f1, support = (
        precision_recall_fscore_support(
            y_true,
            y_pred,
            labels=np.arange(len(class_names)),
            zero_division=0
        )
    )

    return {
        class_name: {
            "precision": p,
            "recall": r,
            "f1": f,
            "support": int(s)
        }
        for class_name, p, r, f, s in zip(
            class_names,
            precision,
            recall,
            f1,
            support
        )
    }
if __name__ == "__main__":

    import pandas as pd
    from sklearn.model_selection import train_test_split

    from ml.preprocessing import preprocess_dataframe
    from ml.predict import load_model, load_encoder

    DATA_PATH = "data/processed/model_dataset.csv"

    print("Loading dataset...")

    # Load the original processed dataset
    df = pd.read_csv(DATA_PATH)

    print(f"Dataset shape: {df.shape}")

    # IMPORTANT:
    # This is exactly how train_rf.py prepares X.
    X = preprocess_dataframe(
        df,
        include_label=False
    )

    # Keep the original labels separately
    y = df["Label"]

    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")

    # Load the SAME encoder used during training
    encoder = load_encoder()

    y_encoded = encoder.transform(y)

    print("\nClass encoding:")

    for label, encoded in zip(
        encoder.classes_,
        encoder.transform(encoder.classes_)
    ):
        print(f"{label} -> {encoded}")

    # Recreate the EXACT same train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.20,
        random_state=42,
        stratify=y_encoded
    )

    print("\nTest set:")
    print(f"X_test: {X_test.shape}")
    print(f"y_test: {y_test.shape}")

    # Same missing-value handling as train_rf.py
    train_medians = X_train.median()

    X_train = X_train.fillna(train_medians)
    X_test = X_test.fillna(train_medians)

    print("\nMissing values:")
    print(f"Testing NaNs: {X_test.isna().sum().sum()}")

    # Load the already-trained model
    model = load_model()

    print("\nModel loaded:")
    print(type(model).__name__)

    # Predict on ORIGINAL test set.
    # Do NOT apply SMOTE to the test set.
    print("\nGenerating predictions...")

    y_pred = model.predict(X_test)

    print(f"Predictions generated: {len(y_pred)}")

    # --------------------------------------------------
    # Overall metrics
    # --------------------------------------------------

    metrics = calculate_metrics(
        y_test,
        y_pred
    )

    print("\n" + "=" * 60)
    print("FINAL MODEL PERFORMANCE")
    print("=" * 60)

    print(
        f"Accuracy:        {metrics['accuracy']:.4f}"
    )

    print(
        f"Accuracy:        {metrics['accuracy'] * 100:.2f}%"
    )

    print(
        f"Macro Precision: {metrics['macro_precision']:.4f}"
    )

    print(
        f"Macro Recall:    {metrics['macro_recall']:.4f}"
    )

    print(
        f"Macro F1:        {metrics['macro_f1']:.4f}"
    )

    # --------------------------------------------------
    # Classification report
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("CLASSIFICATION REPORT")
    print("=" * 60)

    report = get_classification_report(
        y_test,
        y_pred,
        encoder.classes_
    )

    print(report)

    # --------------------------------------------------
    # Confusion matrix
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("CONFUSION MATRIX")
    print("=" * 60)

    cm = get_confusion_matrix(
        y_test,
        y_pred
    )

    print(cm)

    # --------------------------------------------------
    # Class-wise metrics
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("CLASS-WISE METRICS")
    print("=" * 60)

    class_metrics = get_class_metrics(
        y_test,
        y_pred,
        encoder.classes_
    )

    for class_name, values in class_metrics.items():

        print(f"\n{class_name}")
        print(
            f"  Precision: {values['precision']:.4f}"
        )
        print(
            f"  Recall:    {values['recall']:.4f}"
        )
        print(
            f"  F1:        {values['f1']:.4f}"
        )
        print(
            f"  Support:   {values['support']}"
        )