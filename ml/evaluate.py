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