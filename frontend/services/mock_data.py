import pandas as pd
import numpy as np

def generate_mock_dashboard_metrics():
    return {
        "total_traffic": "12,450",
        "total_traffic_change": "+12%",
        "detected_threats": "1,284",
        "detected_threats_change": "+8%",
        "safe_traffic": "11,166",
        "safe_traffic_change": "+14%",
        "threat_rate": "10.3%",
        "threat_rate_change": "-2%"
    }

def generate_mock_attack_distribution():
    return pd.DataFrame({
        "Attack Type": ["Denial of Service (DoS)", "Brute Force", "Port Scanning", "Web Attack", "Other Attacks"],
        "Count": [463, 308, 231, 154, 128],
        "Percentage": [36, 24, 18, 12, 10]
    })

def generate_mock_traffic_history():
    hours = [f"{i}:00" for i in range(24)]
    traffic = np.random.randint(8000, 20000, size=24)
    threats = (traffic * np.random.uniform(0.05, 0.15, size=24)).astype(int)
    return pd.DataFrame({"Time": hours, "Total Traffic": traffic, "Detected Threats": threats})

def generate_mock_recent_predictions():
    return pd.DataFrame([
        {"Time": "10:32 AM", "Source IP": "192.168.1.10", "Destination IP": "10.0.0.5", "Attack Type": "DoS Attack", "Confidence": "96%", "Risk": "HIGH"},
        {"Time": "10:35 AM", "Source IP": "192.168.1.25", "Destination IP": "10.0.0.8", "Attack Type": "Brute Force", "Confidence": "93%", "Risk": "HIGH"},
        {"Time": "10:38 AM", "Source IP": "192.168.1.18", "Destination IP": "10.0.0.12", "Attack Type": "Port Scanning", "Confidence": "87%", "Risk": "MEDIUM"},
        {"Time": "10:40 AM", "Source IP": "192.168.1.33", "Destination IP": "10.0.0.15", "Attack Type": "Normal", "Confidence": "98%", "Risk": "LOW"},
        {"Time": "10:41 AM", "Source IP": "192.168.1.42", "Destination IP": "10.0.0.20", "Attack Type": "Web Attack", "Confidence": "91%", "Risk": "HIGH"},
    ])

def generate_mock_alerts():
    return pd.DataFrame([
        {"Alert ID": "ALT-9021", "Timestamp": "2026-08-19 10:32:45", "Source IP": "192.168.1.105", "Destination IP": "10.0.0.5", "Attack Type": "DoS Attack", "Severity": "HIGH", "Status": "Active"},
        {"Alert ID": "ALT-9022", "Timestamp": "2026-08-19 10:28:17", "Source IP": "192.168.1.203", "Destination IP": "10.0.0.8", "Attack Type": "Brute Force", "Severity": "HIGH", "Status": "Investigating"},
        {"Alert ID": "ALT-9023", "Timestamp": "2026-08-19 10:25:31", "Source IP": "192.168.1.115", "Destination IP": "10.0.0.12", "Attack Type": "Port Scanning", "Severity": "MEDIUM", "Status": "Resolved"},
    ])