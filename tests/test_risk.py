from backend.services.risk_service import calculate_risk


def test_normal_is_low():
    assert calculate_risk("Normal", 0.99) == "LOW"


def test_critical_threshold():
    assert calculate_risk("DDoS", 0.90) == "CRITICAL"


def test_high_threshold():
    assert calculate_risk("DDoS", 0.75) == "HIGH"


def test_medium_threshold():
    assert calculate_risk("DDoS", 0.50) == "MEDIUM"


def test_low_threshold():
    assert calculate_risk("DDoS", 0.49) == "LOW"
