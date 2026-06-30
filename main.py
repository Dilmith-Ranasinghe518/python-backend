import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import modular routers
from auth.routes import router as auth_router
from zoom_clone.routes import router as zoom_clone_router

app = FastAPI(title="Zoom Clone Multi-Backend Services")

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

# Include modular sub-routers
app.include_router(auth_router)
app.include_router(zoom_clone_router)

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Zoom Clone Custom Auth Backend"}
