from typing import Optional
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Request schema for the /predict endpoint."""

    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    protocol: Optional[str] = None
    features: dict


class PredictionResponse(BaseModel):
    """Fixed response contract for the /predict endpoint."""

    attack_type: str
    confidence: float = Field(ge=0.0, le=1.0)
    risk_level: str
