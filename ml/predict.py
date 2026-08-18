import os
import joblib


# Locate the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "intrusion_model.pkl"
)

ENCODER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "label_encoder.pkl"
)


def load_model():
    """Load the trained intrusion detection model."""
    return joblib.load(MODEL_PATH)


def load_encoder():
    """Load the label encoder used during training."""
    return joblib.load(ENCODER_PATH)


def predict(model, encoder, X):
    """
    Predict the intrusion class for the given features.

    Parameters
    ----------
    model : trained model
        Saved Random Forest model.

    encoder : LabelEncoder
        Encoder used during model training.

    X : pandas.DataFrame
        Input feature data.

    Returns
    -------
    numpy.ndarray
        Decoded class labels.
    """

    predictions = model.predict(X)

    return encoder.inverse_transform(predictions)