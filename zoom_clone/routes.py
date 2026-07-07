import os
import time
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt

from auth.routes import get_current_user

router = APIRouter(prefix="/zoom-clone", tags=["zoom-clone"])

STREAM_API_KEY = os.getenv("STREAM_API_KEY", "uehktzarjj8e")
STREAM_SECRET_KEY = os.getenv("STREAM_SECRET_KEY", "e4jf4ta73by5vsa2kqxr62ghbzyban5q3y8dezm9z3tzt5rcy3ymqvfe2r2ygp9j")

@router.get("/")
def zoom_clone_health():
    return {"status": "ok", "message": "Zoom clone features route template"}

@router.get("/token")
def get_stream_token(current_user: dict = Depends(get_current_user)):
    """
    Generates and returns a Stream Video token for the authenticated user.
    """
    if not STREAM_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stream secret key configuration is missing on the server"
        )
    
    user_id = str(current_user["_id"])
    
    # Sign GetStream JWT token
    now = int(time.time())
    payload = {
        "user_id": user_id,
        "iat": now - 60,
        "exp": now + 3600  # Valid for 1 hour
    }
    
    token = jwt.encode(payload, STREAM_SECRET_KEY, algorithm="HS256")
    
    return {
        "stream_token": token,
        "api_key": STREAM_API_KEY,
        "user_id": user_id,
        "username": current_user["username"]
    }
