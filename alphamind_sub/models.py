from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class AdminLoginResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[Dict[str, str]] = None

class TranscriptItem(BaseModel):
    timestamp: str
    text: str

class Resource(BaseModel):
    id: str
    type: str
    question: Optional[str] = None
    answer: Optional[str] = None

class Lesson(BaseModel):
    id: int
    title: str
    duration: Optional[str] = "5m 00s"
    completed: Optional[bool] = False
    videoUrl: Optional[str] = ""
    description: Optional[str] = ""
    objectives: Optional[List[str]] = []
    transcript: Optional[List[TranscriptItem]] = []
    resources: Optional[List[Resource]] = []
    studyMaterials: Optional[List[str]] = []

class Chapter(BaseModel):
    id: int
    title: str
    lessons: List[Lesson] = []

class Course(BaseModel):
    id: Optional[int] = None
    title: str
    instructor: Optional[str] = "Instructor"
    duration: Optional[str] = "1h 00m"
    badge: Optional[str] = "Popular"
    badgeColor: Optional[str] = "bg-purple-100 text-purple-800"
    image: Optional[str] = "bg-gradient-to-br from-purple-500 to-pink-500"
    preview: Optional[str] = ""
    category: Optional[str] = "General"
    chapters: Optional[List[Chapter]] = []
