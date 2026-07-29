from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class ReaderContextModel(BaseModel):
    title: str
    url: str
    content: str
    selected_text: Optional[str] = None

class TutorQuestionRequest(BaseModel):
    prompt: str
    context: Optional[ReaderContextModel] = None
    provider: str = Field(default="gemini")

class TutorQuestionResponse(BaseModel):
    response: str
    provider: str
    grounded: bool

class PageAnalysisRequest(BaseModel):
    context: ReaderContextModel
    mode: str = Field(default="summary") # summary, key_points, quiz, flashcards, explanation

class PageAnalysisResponse(BaseModel):
    title: str
    mode: str
    result: str
