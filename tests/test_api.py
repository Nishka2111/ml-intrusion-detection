def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_predict_valid_request(client):
    payload = {
        "source_ip": "192.168.1.10",
        "destination_ip": "10.0.0.5",
        "protocol": "TCP",
        "features": {"Destination Port": 80, "Flow Duration": 8000000, "Total Fwd Packets": 4200},
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "attack_type" in data
    assert "confidence" in data
    assert "risk_level" in data


def test_predict_invalid_request(client):
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_alerts(client):
    response = client.get("/alerts")
    assert response.status_code == 200


def test_statistics(client):
    response = client.get("/statistics")
    assert response.status_code == 200


def test_traffic_overview(client):
    response = client.get("/traffic-overview")
    assert response.status_code == 200
    data = response.get_json()
    assert "days" in data
    assert "total_traffic" in data


def test_performance(client):
    response = client.get("/performance")
    assert response.status_code == 200
    data = response.get_json()
    assert "accuracy" in data
    assert "precision" in data


def test_analyze_no_file(client):
    response = client.post("/analyze")
    assert response.status_code == 400


def test_analyze_csv(client):
    import io

    csv_data = b"Destination Port,Flow Duration,Total Fwd Packets\n443,120000,8\n80,8000000,4200\n"
    response = client.post(
        "/analyze",
        data={"file": (io.BytesIO(csv_data), "traffic.csv")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["rows_analyzed"] == 2
    assert "attacks_found" in data
    assert "top_attack_type" in data
