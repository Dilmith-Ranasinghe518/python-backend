import os
import uuid
import shutil
import time
import hmac
import hashlib
import base64
import json
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File

STREAM_API_KEY = os.getenv("STREAM_API_KEY", "uehktzarjj8e")
STREAM_SECRET_KEY = os.getenv("STREAM_SECRET_KEY", "e4jf4ta73by5vsa2kqxr62ghbzyban5q3y8dezm9z3tzt5rcy3ymqvfe2r2ygp9j")

def _base64url_encode(input_bytes: bytes) -> str:
    return base64.urlsafe_b64encode(input_bytes).decode('utf-8').rstrip('=')

def generate_stream_token(user_id: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    payload = {
        "user_id": user_id,
        "iat": now - 60,
        "exp": now + 3600 * 24
    }
    
    header_b64 = _base64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    payload_b64 = _base64url_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))
    
    signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
    signature = hmac.new(STREAM_SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()
    signature_b64 = _base64url_encode(signature)
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

router = APIRouter()
from alphamind_sub.models import (
    AdminLoginRequest, AdminLoginResponse, Course, CoursesPageData,
    BooksPageData, ShortNotesPageData, RevisionPageData, ExamHubPageData, AuthConfigData,
    UserRegisterRequest, UserLoginRequest, UserForgotPasswordRequest, AuthUserResponse
)
from alphamind_sub.store import (
    get_all_courses,
    get_course_by_id,
    save_or_update_course,
    delete_course_by_id,
    get_courses_page_data,
    save_courses_page_data,
    get_books_page_data,
    save_books_page_data,
    get_short_notes_page_data,
    save_short_notes_page_data,
    get_revision_page_data,
    save_revision_page_data,
    get_exam_hub_page_data,
    save_exam_hub_page_data,
    get_auth_config_data,
    save_auth_config_data,
    register_user,
    login_user,
    forgot_password_user
)

router = APIRouter()

ADMIN_USERNAME = os.getenv("ALPHAMIND_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ALPHAMIND_ADMIN_PASS", "admin123")
ADMIN_TOKEN = "alphamind-admin-secret-token-2026"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

@router.post("/admin/login", response_model=AdminLoginResponse)
def admin_login(req: AdminLoginRequest):
    if req.username == ADMIN_USERNAME and req.password == ADMIN_PASSWORD:
        return AdminLoginResponse(
            success=True,
            message="Login successful",
            token=ADMIN_TOKEN,
            user={"username": req.username, "role": "admin"}
        )
    raise HTTPException(status_code=401, detail="Invalid admin username or password")

# --- Structured Courses Page API Endpoints ---
@router.get("/courses-page")
def get_courses_page():
    data = get_courses_page_data()
    return {"success": True, "data": data}

@router.post("/courses-page")
def update_courses_page(data: CoursesPageData):
    payload = data.model_dump()
    saved = save_courses_page_data(payload)
    return {"success": True, "message": "Courses page data saved successfully", "data": saved}

# --- Structured Books Page API Endpoints ---
@router.get("/books-page")
def get_books_page():
    data = get_books_page_data()
    return {"success": True, "data": data}

@router.post("/books-page")
def update_books_page(data: BooksPageData):
    payload = data.model_dump()
    saved = save_books_page_data(payload)
    return {"success": True, "message": "Books page data saved successfully", "data": saved}

# --- Structured Short Notes Page API Endpoints ---
@router.get("/short-notes-page")
def get_short_notes_page():
    data = get_short_notes_page_data()
    return {"success": True, "data": data}

@router.post("/short-notes-page")
def update_short_notes_page(data: ShortNotesPageData):
    payload = data.model_dump()
    saved = save_short_notes_page_data(payload)
    return {"success": True, "message": "Short notes page data saved successfully", "data": saved}

# --- Structured Revision Page API Endpoints ---
@router.get("/revision-page")
def get_revision_page():
    data = get_revision_page_data()
    return {"success": True, "data": data}

@router.post("/revision-page")
def update_revision_page(data: RevisionPageData):
    payload = data.model_dump()
    saved = save_revision_page_data(payload)
    return {"success": True, "message": "Revision page data saved successfully", "data": saved}

# --- Exam Hub Page Endpoints ---
@router.get("/exam-hub-page")
def get_exam_hub_page():
    data = get_exam_hub_page_data()
    return {"success": True, "data": data}

@router.post("/exam-hub-page")
def update_exam_hub_page(data: ExamHubPageData):
    payload = data.model_dump()
    saved = save_exam_hub_page_data(payload)
    return {"success": True, "message": "Exam Hub page data saved successfully", "data": saved}

# --- Auth Config Endpoints ---
@router.get("/auth-config")
def get_auth_config():
    data = get_auth_config_data()
    return {"success": True, "data": data}

@router.post("/auth-config")
def update_auth_config(data: AuthConfigData):
    payload = data.model_dump()
    saved = save_auth_config_data(payload)
    return {"success": True, "message": "Auth config saved successfully", "data": saved}

# --- User Auth Endpoints ---
@router.post("/user/register", response_model=AuthUserResponse)
def user_register(req: UserRegisterRequest):
    result = register_user(req.fullName, req.identifier, req.password)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return AuthUserResponse(**result)

@router.post("/user/login", response_model=AuthUserResponse)
def user_login(req: UserLoginRequest):
    result = login_user(req.identifier, req.password)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return AuthUserResponse(**result)

@router.post("/user/forgot-password", response_model=AuthUserResponse)
def user_forgot_password(req: UserForgotPasswordRequest):
    result = forgot_password_user(req.identifier, req.newPassword)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return AuthUserResponse(**result)

@router.get("/stream-token")
def get_stream_token(userId: str):
    if not userId or not userId.strip():
        raise HTTPException(status_code=400, detail="userId parameter is required")
    token = generate_stream_token(userId.strip())
    return {"success": True, "token": token, "apiKey": STREAM_API_KEY}

# --- Image Upload Endpoint ---
@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")
    
    file_ext = os.path.splitext(file.filename)[1] or ".jpg"
    filename = f"{uuid.uuid4().hex}{file_ext.lower()}"
    file_path = os.path.join(UPLOADS_DIR, filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {str(e)}")
    
    image_url = f"/uploads/{filename}"
    return {"success": True, "url": image_url, "filename": filename}

# --- Legacy Endpoints for backward compatibility ---
@router.get("/courses")
def list_courses():
    return {"success": True, "courses": get_all_courses()}

@router.get("/courses/{course_id}")
def get_course(course_id: int):
    course = get_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"success": True, "course": course}

@router.post("/courses")
def create_course(course: Course):
    course_data = course.model_dump()
    saved = save_or_update_course(course_data)
    return {"success": True, "message": "Course created successfully", "course": saved}

@router.put("/courses/{course_id}")
def update_course(course_id: int, course: Course):
    course_data = course.model_dump()
    course_data["id"] = course_id
    saved = save_or_update_course(course_data)
    return {"success": True, "message": "Course updated successfully", "course": saved}

@router.delete("/courses/{course_id}")
def delete_course(course_id: int):
    success = delete_course_by_id(course_id)
    if not success:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"success": True, "message": "Course deleted successfully"}
