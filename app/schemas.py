from pydantic import BaseModel
from typing import List

class RecommendationItem(BaseModel):
    category: str
    confidence: float
    color: str
    description: str

class RecommendationResponse(BaseModel):
    items: List[RecommendationItem]
    message: str
