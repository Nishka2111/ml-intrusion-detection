from backend.app import app


def main():
    # Load the trained model so we can get its exact feature names.
    from backend.services.prediction_service import _load_model

    model = _load_model()

    # Create 78 dummy feature values.
    features = {
        feature_name: 0.0
        for feature_name in model.feature_names_in_
    }

    payload = {
        "source_ip": "192.168.1.10",
        "destination_ip": "192.168.1.20",
        "protocol": "TCP",
        "features": features,
    }

    print("Sending POST /predict...")
    print(f"Number of features: {len(features)}")

    with app.test_client() as client:
        response = client.post(
            "/predict",
            json=payload,
        )

        print("\n==============================")
        print("API RESPONSE")
        print("==============================")
        print("Status code:", response.status_code)
        print("Response:")
        print(response.get_json())
        print("==============================")


if __name__ == "__main__":
    main()