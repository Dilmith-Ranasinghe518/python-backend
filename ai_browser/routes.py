from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from ai_browser.models import (
    TutorQuestionRequest,
    TutorQuestionResponse,
    PageAnalysisRequest,
    PageAnalysisResponse
)
from ai_browser.services import (
    answer_tutor_question,
    build_summary,
    build_key_points,
    build_quiz,
    build_flashcards,
    build_explanation
)

router = APIRouter(prefix="/api/ai-browser", tags=["ai-browser"])

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI Browser FastAPI Service"
    }

@router.post("/chat", response_model=TutorQuestionResponse)
def tutor_chat(req: TutorQuestionRequest):
    """
    Grounded AI Tutor Chat endpoint for AI Browser.
    """
    title = req.context.title if req.context else ""
    content = req.context.content if req.context else ""

    res = answer_tutor_question(
        prompt=req.prompt,
        title=title,
        content=content,
        provider=req.provider
    )

    return TutorQuestionResponse(
        response=res["response"],
        provider=res["provider"],
        grounded=res["grounded"]
    )

@router.post("/analyze", response_model=PageAnalysisResponse)
def analyze_page(req: PageAnalysisRequest):
    """
    Page Analysis Endpoint (Summary, Key Points, Quiz, Flashcards, Explanation).
    """
    title = req.context.title
    content = req.context.content
    mode = (req.mode or "summary").lower()

    if mode == "summary":
        result = build_summary(title, content)
    elif mode == "key_points":
        result = build_key_points(title, content)
    elif mode == "quiz":
        result = build_quiz(title, content)
    elif mode == "flashcards":
        result = build_flashcards(title, content)
    elif mode == "explanation":
        result = build_explanation(title, content)
    else:
        result = build_summary(title, content)

    return PageAnalysisResponse(
        title=title,
        mode=mode,
        result=result
    )
