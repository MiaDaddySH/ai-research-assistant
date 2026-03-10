from pydantic import BaseModel
from typing import List


class ResearchRequest(BaseModel):
    question: str


class SourceItem(BaseModel):
    title: str
    url: str


class ResearchResponse(BaseModel):
    question: str
    summary: str
    key_points: List[str]
    sources: List[SourceItem]