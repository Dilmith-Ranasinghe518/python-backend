import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bson import ObjectId
from typing import Optional

from database import users_collection
from models import UserRegister, UserLogin, UserResponse, Token
from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_access_token
)

app = FastAPI(title="Zoom Clone Auth Backend")

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://zoom-clone-ten-rose.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer(auto_error=False)

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    token = credentials.credentials
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid"
        )
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format"
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Zoom Clone Custom Auth Backend"}

@app.post("/auth/register", response_model=UserResponse)
def register(user_data: UserRegister):
    # Check for existing user by email
    if users_collection.find_one({"email": user_data.email.strip().lower()}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # Check for existing user by username
    if users_collection.find_one({"username": user_data.username.strip()}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Generate default avatar
    avatar_url = f"https://api.dicebear.com/7.x/initials/svg?seed={user_data.username.strip()}"
    
    hashed_pwd = get_password_hash(user_data.password)
    user_dict = {
        "username": user_data.username.strip(),
        "email": user_data.email.strip().lower(),
        "hashed_password": hashed_pwd,
        "imageUrl": avatar_url
    }
    
    result = users_collection.insert_one(user_dict)
    
    return {
        "id": str(result.inserted_id),
        "username": user_dict["username"],
        "email": user_dict["email"],
        "imageUrl": user_dict["imageUrl"]
    }

@app.post("/auth/login")
def login(user_data: UserLogin):
    # Find user by username or email
    login_term = user_data.username_or_email.strip()
    user = users_collection.find_one({
        "$or": [
            {"username": login_term},
            {"email": login_term.lower()}
        ]
    })
    
    if not user or not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
        
    # Generate token
    token_data = {
        "sub": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]
    }
    access_token = create_access_token(data=token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"],
            "imageUrl": user.get("imageUrl")
        }
    }

@app.get("/auth/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": str(current_user["_id"]),
        "username": current_user["username"],
        "email": current_user["email"],
        "imageUrl": current_user.get("imageUrl")
    }
