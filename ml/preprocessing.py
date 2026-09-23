import pandas as pd
import numpy as np


# Exact feature schema used by the trained Random Forest
MODEL_FEATURES = [
    "Destination Port",
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Fwd Packet Length Max",
    "Fwd Packet Length Min",
    "Fwd Packet Length Mean",
    "Fwd Packet Length Std",
    "Bwd Packet Length Max",
    "Bwd Packet Length Min",
    "Bwd Packet Length Mean",
    "Bwd Packet Length Std",
    "Flow Bytes/s",
    "Flow Packets/s",
    "Flow IAT Mean",
    "Flow IAT Std",
    "Flow IAT Max",
    "Flow IAT Min",
    "Fwd IAT Total",
    "Fwd IAT Mean",
    "Fwd IAT Std",
    "Fwd IAT Max",
    "Fwd IAT Min",
    "Bwd IAT Total",
    "Bwd IAT Mean",
    "Bwd IAT Std",
    "Bwd IAT Max",
    "Bwd IAT Min",
    "Fwd PSH Flags",
    "Bwd PSH Flags",
    "Fwd URG Flags",
    "Bwd URG Flags",
    "Fwd Header Length",
    "Bwd Header Length",
    "Fwd Packets/s",
    "Bwd Packets/s",
    "Min Packet Length",
    "Max Packet Length",
    "Packet Length Mean",
    "Packet Length Std",
    "Packet Length Variance",
    "FIN Flag Count",
    "SYN Flag Count",
    "RST Flag Count",
    "PSH Flag Count",
    "ACK Flag Count",
    "URG Flag Count",
    "CWE Flag Count",
    "ECE Flag Count",
    "Down/Up Ratio",
    "Average Packet Size",
    "Avg Fwd Segment Size",
    "Avg Bwd Segment Size",
    "Fwd Header Length.1",
    "Fwd Avg Bytes/Bulk",
    "Fwd Avg Packets/Bulk",
    "Fwd Avg Bulk Rate",
    "Bwd Avg Bytes/Bulk",
    "Bwd Avg Packets/Bulk",
    "Bwd Avg Bulk Rate",
    "Subflow Fwd Packets",
    "Subflow Fwd Bytes",
    "Subflow Bwd Packets",
    "Subflow Bwd Bytes",
    "Init_Win_bytes_forward",
    "Init_Win_bytes_backward",
    "act_data_pkt_fwd",
    "min_seg_size_forward",
    "Active Mean",
    "Active Std",
    "Active Max",
    "Active Min",
    "Idle Mean",
    "Idle Std",
    "Idle Max",
    "Idle Min"
]


def clean_dataframe(df):
    """Clean a raw network-flow dataframe."""

    df = df.copy()

    # Remove whitespace from column names
    df.columns = df.columns.str.strip()

    # Replace infinite values with NaN
    df = df.replace([np.inf, -np.inf], np.nan)

    return df


def map_attack_label(label):
    """Map original CICIDS2017 labels to project classes."""

    label = str(label).strip()

    if label == "BENIGN":
        return "BENIGN"

    if label.startswith("DoS "):
        return "DoS"

    if label == "DDoS":
        return "DDoS"

    if label == "PortScan":
        return "PortScan"

    if label in ["FTP-Patator", "SSH-Patator"]:
        return "Brute Force"

    if "Web Attack" in label and "Brute Force" in label:
        return "Brute Force"

    if label == "Bot":
        return "Bot"

    if "Web Attack" in label:
        return "Web Attack"

    return "EXCLUDE"


def preprocess_dataframe(df, include_label=False):
    """
    Prepare network-flow data for the ML model.

    Returns exactly the 78 features expected by the model.
    """

    df = clean_dataframe(df)

    if include_label and "Label" in df.columns:
        df["Label"] = df["Label"].apply(map_attack_label)

        df = df[df["Label"] != "EXCLUDE"].copy()

    # Check for missing model features
    missing_features = [
        feature for feature in MODEL_FEATURES
        if feature not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    # Keep only the features used by the model
    X = df[MODEL_FEATURES].copy()

    # Handle missing values
    X = X.fillna(X.median())

    return X