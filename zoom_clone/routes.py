from fastapi import APIRouter

router = APIRouter(prefix="/zoom-clone", tags=["zoom-clone"])

@router.get("/")
def zoom_clone_health():
    return {"status": "ok", "message": "Zoom clone features route template"}
