from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class AdminLoginResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[Dict[str, str]] = None

class CarouselItem(BaseModel):
    id: str
    name: str
    image: str
    badge: Optional[str] = "Popular"
    pill: Optional[str] = "Free with Plus"

class Subcontent(BaseModel):
    id: str
    title: str
    duration: Optional[str] = "5m 00s"
    completed: Optional[bool] = False
    videoUrl: Optional[str] = ""
    description: Optional[str] = ""
    resources: Optional[List[Dict[str, Any]]] = []
    studyMaterials: Optional[List[str]] = []

class Content(BaseModel):
    id: str
    subjectId: str
    title: str
    subcontents: List[Subcontent] = []

class ContentCard(BaseModel):
    id: str
    subcontentId: str
    title: str
    subtitle: Optional[str] = ""
    description: Optional[str] = ""
    image: Optional[str] = ""
    badge: Optional[str] = "Best seller"
    learners: Optional[str] = "133,854"
    rating: Optional[str] = "95% (2.65K)"
    pill: Optional[str] = "Free with Plus"
    price: Optional[str] = "520"
    ratingValue: Optional[str] = "4.8"

class CoursesPageData(BaseModel):
    heroImage: Optional[str] = "/images/Poster1.jpg"
    carouselItems: List[CarouselItem] = []
    contents: List[Content] = []
    contentCards: List[ContentCard] = []

class BooksPageData(BaseModel):
    heroImage: Optional[str] = "/images/Poster1.jpg"
    carouselItems: List[CarouselItem] = []
    contents: List[Content] = []
    contentCards: List[ContentCard] = []

# Legacy Models for backward compatibility
class Lesson(BaseModel):
    id: int
    title: str
    duration: Optional[str] = "5m 00s"
    completed: Optional[bool] = False
    videoUrl: Optional[str] = ""
    description: Optional[str] = ""
    resources: Optional[List[Dict[str, Any]]] = []
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
    heroImage: Optional[str] = "/images/Poster1.jpg"
    preview: Optional[str] = ""
    category: Optional[str] = "General"
    chapters: Optional[List[Chapter]] = []
