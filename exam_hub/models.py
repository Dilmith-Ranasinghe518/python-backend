from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class MCQOption(BaseModel):
    q: str
    options: List[str]

class CreatePaperRequest(BaseModel):
    subject: str = Field(default="General Science")
    year: Optional[int] = None
    language: str = Field(default="English")
    provider: str = Field(default="template")

class GradeMCQRequest(BaseModel):
    paper_id: int
    answers: Dict[str, str] = Field(default_factory=dict)

class PaperSummary(BaseModel):
    id: int
    title: str
    subject: str
    year: int
    language: str
    source: str
    created_at: str

class PaperDetail(BaseModel):
    id: int
    title: str
    subject: str
    year: int
    language: str
    source: str
    created_at: str
    content_markdown: str
    mcq: Optional[List[Dict[str, Any]]] = None
