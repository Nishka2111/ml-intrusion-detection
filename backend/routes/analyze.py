import csv
import io
import time
from flask import Blueprint, jsonify, request

from backend.database.database import db
from backend.database.models import IntrusionLog
from backend.services.prediction_service import predict_intrusion
from backend.services.risk_service import calculate_risk

analyze_bp = Blueprint("analyze", __name__)


@analyze_bp.post("/analyze")
def analyze_traffic():
    """Analyze an uploaded traffic file (CSV / txt of feature rows).

    Each row is treated as a connection, sent through the ML prediction
    service, saved to the database, and aggregate stats + sample predictions are returned.
    """
    file = request.files.get("file")
    if file is None:
        return jsonify({
            "error": "No file uploaded",
            "details": "Provide a file via multipart form field 'file'."
        }), 400

    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ("csv", "txt"):
        return jsonify({
            "error": "Unsupported file type",
            "details": "Only .csv or .txt feature files are supported."
        }), 400

    try:
        raw = file.read().decode("utf-8", errors="ignore")
    except UnicodeDecodeError:
        return jsonify({
            "error": "Invalid file encoding",
            "details": "File must be UTF-8 text."
        }), 400

    rows = _parse_rows(raw, ext)
    if not rows:
        return jsonify({
            "error": "No usable rows",
            "details": "The uploaded file contained no parseable feature rows."
        }), 422

    start = time.perf_counter()

    attack_counts: dict[str, int] = {}
    total_attacks = 0
    total_rows = 0
    sample_predictions: list[dict] = []

    for idx, row in enumerate(rows):
        result = predict_intrusion(row)
        attack_type = result["attack_type"]
        confidence = result["confidence"]
        risk_level = calculate_risk(attack_type, confidence)

        src_ip = row.get("source_ip") or row.get("Source IP") or f"192.168.1.{10 + (idx % 200)}"
        dst_ip = row.get("destination_ip") or row.get("Destination IP") or f"10.0.0.{5 + (idx % 100)}"
        protocol = row.get("protocol") or row.get("Protocol") or "TCP"

        log = IntrusionLog(
            source_ip=src_ip,
            destination_ip=dst_ip,
            protocol=protocol,
            attack_type=attack_type,
            confidence=confidence,
            risk_level=risk_level,
        )
        db.session.add(log)
        total_rows += 1

        if attack_type.lower() != "normal":
            total_attacks += 1
            attack_counts[attack_type] = attack_counts.get(attack_type, 0) + 1
        else:
            attack_counts["Normal"] = attack_counts.get("Normal", 0) + 1

        if idx < 20:
            sample_predictions.append({
                "row_id": idx + 1,
                "source_ip": src_ip,
                "destination_ip": dst_ip,
                "protocol": protocol,
                "attack_type": attack_type,
                "confidence": round(confidence * 100, 2),
                "risk_level": risk_level,
            })

    db.session.commit()

    elapsed = round(time.perf_counter() - start, 3)
    non_normal = {k: v for k, v in attack_counts.items() if k.lower() != "normal"}
    top_attack = max(non_normal.items(), key=lambda x: x[1])[0] if non_normal else "None (All Normal)"

    return jsonify({
        "rows_analyzed": total_rows,
        "attacks_found": total_attacks,
        "normal_traffic": total_rows - total_attacks,
        "top_attack_type": top_attack,
        "processing_time_sec": elapsed,
        "attack_breakdown": attack_counts,
        "predictions": sample_predictions,
    }), 200


def _parse_rows(raw: str, ext: str) -> list[dict]:
    """Parse uploaded text into a list of feature dicts."""
    if ext == "csv":
        return _parse_csv(raw)
    try:
        return _parse_csv(raw)
    except Exception:
        return [{"feature": line.strip()} for line in raw.splitlines() if line.strip()]


def _parse_csv(raw: str) -> list[dict]:
    reader = csv.DictReader(io.StringIO(raw))
    rows: list[dict] = []
    for row in reader:
        cleaned = {k: v for k, v in row.items() if v is not None and v != ""}
        if cleaned:
            rows.append(cleaned)
    return rows
