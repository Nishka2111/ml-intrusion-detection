from backend.services.prediction_service import (
    _load_model,
    predict_intrusion,
)


def main():
    print("Loading trained model...")

    model = _load_model()

    print(f"Model: {type(model).__name__}")
    print(f"Expected features: {model.n_features_in_}")

    # Create a dictionary containing all 78 model features.
    # Values are set to 0 only for integration testing.
    features = {
        feature_name: 0.0
        for feature_name in model.feature_names_in_
    }

    print("\nRunning prediction...")

    result = predict_intrusion(features)

    print("\n==============================")
    print("PREDICTION RESULT")
    print("==============================")
    print(f"Attack Type : {result['attack_type']}")
    print(f"Confidence  : {result['confidence']:.4f}")
    print("==============================")


if __name__ == "__main__":
    main()