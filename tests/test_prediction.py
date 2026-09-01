from backend.services.prediction_service import predict_intrusion


def test_returns_contract():
    result = predict_intrusion({"Destination Port": 80})
    assert set(result) == {"attack_type", "confidence"}
    assert 0.0 <= result["confidence"] <= 1.0
    assert isinstance(result["attack_type"], str)


def test_heuristic_classifies_ddos():
    result = predict_intrusion({
        "Destination Port": 80, "Flow Duration": 8_000_000,
        "Total Fwd Packets": 4200, "Total Backward Packets": 3900,
        "Total Length Of Fwd Packets": 630000, "Total Length Of Bwd Packets": 400000,
        "SYN Flag Count": 5, "Flow Bytes/s": 1_200_000,
    })
    assert result["attack_type"] in ("DoS Attack", "DDoS")
    assert result["confidence"] >= 0.90


def test_heuristic_classifies_normal():
    result = predict_intrusion({
        "Destination Port": 443, "Flow Duration": 120_000,
        "Total Fwd Packets": 8, "Total Backward Packets": 10,
        "Total Length Of Fwd Packets": 3400, "Total Length Of Bwd Packets": 5200,
        "Packet Length Std": 210, "SYN Flag Count": 1,
        "Flow Bytes/s": 71_000,
    })
    assert result["attack_type"] == "Normal"
    assert result["confidence"] >= 0.90
