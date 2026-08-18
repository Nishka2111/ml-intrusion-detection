import pandas as pd

from ml.preprocessing import preprocess_dataframe
from ml.predict import load_model, load_encoder, predict


DATA_PATH = "data/processed/model_dataset.csv"


def main():
    print("Loading test data...")

    df = pd.read_csv(DATA_PATH).head(10)

    X = preprocess_dataframe(df)

    model = load_model()
    encoder = load_encoder()

    predictions = predict(
        model,
        encoder,
        X
    )

    print(f"Input shape: {X.shape}")
    print("Predictions:")

    for prediction in predictions:
        print(f"- {prediction}")


if __name__ == "__main__":
    main()