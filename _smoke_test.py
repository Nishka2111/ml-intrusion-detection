"""Live end-to-end smoke test verifying Flask REST backend & frontend api_client."""

from __future__ import annotations

import os
import sys
import time
import requests

__test__ = False

sys.path.insert(0, os.path.join(os.getcwd(), "frontend"))

BASE = "http://127.0.0.1:5000"

# 1. Health Endpoint
r = requests.get(f"{BASE}/health")
print("GET /health:", r.status_code, r.json())
assert r.status_code == 200 and r.json()["status"] == "ok"

# 2. Predict Endpoint (Normal Flow)
payload = {
    "source_ip": "192.168.1.10",
    "destination_ip": "10.0.0.5",
    "protocol": "TCP",
    "features": {
        "Destination Port": 443, "Flow Duration": 120000,
        "Total Fwd Packets": 8, "Total Backward Packets": 10,
        "Total Length of Fwd Packets": 3400, "Total Length of Bwd Packets": 5200,
        "Packet Length Std": 210, "SYN Flag Count": 1, "Flow Bytes/s": 71000.0,
    },
}
r = requests.post(f"{BASE}/predict", json=payload)
print("POST /predict (Normal):", r.status_code, r.json())
assert r.status_code == 200 and r.json()["attack_type"] == "Normal"

# 3. Predict Endpoint (DDoS Threat)
payload["features"] = {
    "Destination Port": 80, "Flow Duration": 8000000,
    "Total Fwd Packets": 4200, "Total Backward Packets": 3900,
    "Total Length of Fwd Packets": 630000, "Total Length of Bwd Packets": 400000,
    "SYN Flag Count": 5, "Flow Bytes/s": 1200000.0,
}
r = requests.post(f"{BASE}/predict", json=payload)
print("POST /predict (DDoS):", r.status_code, r.json())
assert r.status_code == 200 and r.json()["attack_type"] in ("DDoS", "DoS Attack")

# 4. Predict Endpoint (Pydantic Invalid Request Validation)
r = requests.post(f"{BASE}/predict", json={})
print("POST /predict (Invalid):", r.status_code)
assert r.status_code == 422

# 5. Read endpoints
for endpoint in ["/statistics", "/logs", "/traffic-overview", "/alerts", "/performance"]:
    r = requests.get(f"{BASE}{endpoint}")
    print(f"GET {endpoint}:", r.status_code)
    assert r.status_code == 200

# 6. Analyze CSV File Upload
csv_data = b"Destination Port,Flow Duration,Total Fwd Packets,Total Backward Packets\n443,120000,8,10\n80,8000000,4200,3900\n"
r = requests.post(f"{BASE}/analyze", files={"file": ("traffic.csv", csv_data, "text/csv")})
print("POST /analyze:", r.status_code, r.json())
assert r.status_code == 200 and r.json()["rows_analyzed"] == 2

# 7. Frontend API Client Integration Test
from services import api_client

print("api_client.backend_online():", api_client.backend_online())
res = api_client.predict_traffic({
    "Destination Port": 22, "Flow Duration": 400000,
    "Total Fwd Packets": 30, "Total Backward Packets": 28,
    "Total Length of Fwd Packets": 4200, "Total Length of Bwd Packets": 3800,
    "SYN Flag Count": 12, "Flow Bytes/s": 21000.0,
})
print("api_client.predict_traffic:", res)
assert res["status"] == "Intrusion Detected"

dash = api_client.get_dashboard_data()
print("api_client.get_dashboard_data() metrics:", dash["metrics"])
assert int(dash["metrics"]["detected_threats"]) > 0

print("SMOKE TEST PASSED SUCCESSFULLY!")
