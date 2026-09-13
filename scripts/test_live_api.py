import json
import urllib.request

from backend.services.prediction_service import _load_model


def main():
    model = _load_model()

    # Create exactly the 78 features expected by the model.
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

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        "http://127.0.0.1:5000/predict",
        data=data,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    print("Sending HTTP POST /predict...")

    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8")

            print("\n==============================")
            print("LIVE API RESPONSE")
            print("==============================")
            print("Status code:", response.status)
            print("Response:")
            print(json.dumps(json.loads(body), indent=2))
            print("==============================")

    except urllib.error.HTTPError as error:
        print("\nHTTP ERROR:", error.code)
        print(error.read().decode("utf-8"))

    except Exception as error:
        print("\nCONNECTION ERROR:")
        print(error)


if __name__ == "__main__":
    main()