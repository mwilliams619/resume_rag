from pydantic import BaseModel
from typing import Optional

class JobDescription(BaseModel):
    text: str

class OptimizationQuery(BaseModel):
    query: str

class OptimizationResponse(BaseModel):
    response: str
    error: Optional[str] = None