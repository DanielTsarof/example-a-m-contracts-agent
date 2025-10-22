from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class InvokePayload(BaseModel):
    thread_id: str = Field(default="demo-001")
    acquirer: Dict[str, Any] = Field(default_factory=lambda: {"id": "ACQ"})
    target: Dict[str, Any] = Field(default_factory=lambda: {"id": "TGT"})
    market: Optional[Dict[str, Any]] = None
    financials: Optional[Dict[str, Any]] = None
    macro: Optional[Dict[str, Any]] = None


class ResumePayload(BaseModel):
    thread_id: str
    approve: bool
