"""Risk assessment logic converting prediction + confidence into risk levels."""

from __future__ import annotations


def calculate_risk(attack_type: str, confidence: float) -> str:
    """Calculate risk level: CRITICAL, HIGH, MEDIUM, LOW."""
    if not attack_type or attack_type.strip().lower() == "normal":
        return "LOW"

    if confidence >= 0.90:
        return "CRITICAL"
    if confidence >= 0.75:
        return "HIGH"
    if confidence >= 0.50:
        return "MEDIUM"

    return "LOW"
