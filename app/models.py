from pydantic import BaseModel, Field
from typing import Dict, Any
from enum import Enum

class MethodUsed(str, Enum):
    llm_primary = "llm_primary"
    healthcare_ai = "healthcare_ai"

class ClinicalNote(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000)

class ClinicalResponse(BaseModel):
    structured_data: Dict[str, Any]
    summary: str
    confidence_score: float
    processing_time_ms: float
    method_used: MethodUsed
    message: str
