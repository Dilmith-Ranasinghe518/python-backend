from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form

from exam_hub.models import (
    CreatePaperRequest,
    GradeMCQRequest
)
from exam_hub.store import list_papers, get_paper, create_paper
from exam_hub.generator import generate_practice_paper
from exam_hub.marker import simple_mark
from exam_hub.text_extract import extract_text_from_upload

router = APIRouter(prefix="/api/exam-hub", tags=["exam-hub"])

@router.get("/papers")
def get_papers():
    """
    Returns the list of available exam papers.
    """
    return list_papers()

@router.get("/papers/{paper_id}")
def get_paper_by_id(paper_id: int):
    """
    Retrieves detailed paper information by paper_id.
    """
    if paper_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid paper id"
        )
    paper = get_paper(paper_id)
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found"
        )
    return {
        "id": paper["id"],
        "title": paper["title"],
        "subject": paper["subject"],
        "year": paper["year"],
        "language": paper["language"],
        "source": paper["source"],
        "created_at": paper["created_at"],
        "content_markdown": paper["content_markdown"],
        "mcq": paper.get("mcq")
    }

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_new_paper(req: CreatePaperRequest):
    """
    Generates and creates a new practice exam paper.
    """
    subject = (req.subject or "General Science").strip()
    year = req.year if req.year else datetime.now().year
    language = (req.language or "English").strip()
    provider = req.provider or "template"

    gen = generate_practice_paper(subject=subject, year=year, language=language, provider=provider)
    title = f"G.C.E. O/L {subject} {year} (Practice) — {language}"

    paper = create_paper({
        "title": title,
        "subject": subject,
        "year": year,
        "language": language,
        "source": gen["source"],
        "content_markdown": gen["content_markdown"],
        "mcq": gen["mcq"],
        "mcq_answer_key": gen["mcq_answer_key"],
        "marking_rubric": (
            "Marking guidance:\n"
            "- MCQ: 1 mark each.\n"
            "- Structured: award marks for correct facts, steps, and clarity.\n"
            "- Essay: award marks for key points, explanations, and logical structure.\n"
        )
    })

    return {
        "id": paper["id"],
        "title": paper["title"],
        "subject": paper["subject"],
        "year": paper["year"],
        "language": paper["language"],
        "source": paper["source"],
        "created_at": paper["created_at"],
        "content_markdown": paper["content_markdown"],
        "mcq": paper.get("mcq")
    }

@router.post("/grade-mcq")
def grade_mcq(req: GradeMCQRequest):
    """
    Grades user answers against the paper's MCQ answer key.
    """
    paper_id = req.paper_id
    answers = req.answers or {}

    if paper_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid paper id"
        )

    paper = get_paper(paper_id)
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found"
        )

    key = paper.get("mcq_answer_key")
    if not key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This paper does not have an MCQ answer key"
        )

    total = len(key)
    correct = 0
    results: Dict[str, Dict[str, Any]] = {}

    for q_idx, correct_opt in key.items():
        selected = str(answers.get(q_idx) or "").strip().upper()
        correct_str = str(correct_opt).strip().upper()
        is_correct = (selected == correct_str)
        if is_correct:
            correct += 1
        results[q_idx] = {
            "selected": selected if selected else None,
            "correct": correct_opt,
            "is_correct": is_correct
        }

    return {
        "paper_id": paper_id,
        "correct": correct,
        "total": total,
        "results": results
    }

@router.post("/submit-written")
async def submit_written(
    paper_id: int = Form(...),
    question_type: str = Form(...),
    question_number: Optional[int] = Form(None),
    provider: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    """
    Extracts text from uploaded file and evaluates written answer.
    """
    if paper_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid paper id"
        )

    qtype = (question_type or "").strip().lower()
    if qtype not in ["structured", "essay"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid question type"
        )

    paper = get_paper(paper_id)
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found"
        )

    extracted_text = await extract_text_from_upload(file)

    marking = simple_mark(
        extracted_text=extracted_text,
        question_type=qtype,
        question_number=question_number,
        paper_markdown=paper.get("content_markdown", "")
    )

    return {
        "paper_id": paper_id,
        "question_type": qtype,
        "question_number": question_number,
        "extracted_text": extracted_text,
        "feedback": marking["feedback"]
    }
