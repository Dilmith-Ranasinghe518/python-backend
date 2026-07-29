from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class MessageItem(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[MessageItem]
    temperature: float = Field(default=0.7)
    response_language: str = Field(default="English")
    forced_provider: Optional[str] = None
    forced_model: Optional[str] = None
    user_gemini_key: Optional[str] = None
    user_openai_key: Optional[str] = None
    max_tokens: int = Field(default=2048)

class ChatResponse(BaseModel):
    reply: str
    provider: str
    provider_label: str
    model: str

class RAGQueryRequest(BaseModel):
    query: str
    documents: List[Dict[str, Any]] = Field(default_factory=list)
    top_k: int = Field(default=3)

class RAGQueryResponse(BaseModel):
    answer: str
    citations: List[Dict[str, Any]] = Field(default_factory=list)
