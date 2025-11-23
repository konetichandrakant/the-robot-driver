from pydantic import BaseModel
from typing import Any
from enum import Enum

class AutomationRequest(BaseModel):
    user_query: str

class AutomationResponse(BaseModel):
    tool: str
    params: dict[Any, Any] | None = None
    reasoning: str