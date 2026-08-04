import os
import uuid
import shutil
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File
from alphamind_sub.models import AdminLoginRequest, AdminLoginResponse, Course, CoursesPageData
from alphamind_sub.store import (
    get_all_courses,
    get_course_by_id,
    save_or_update_course,
    delete_course_by_id,
    get_courses_page_data,
    save_courses_page_data
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
