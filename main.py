import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import modular routers
from auth.routes import router as auth_router
from zoom_clone.routes import router as zoom_clone_router
from whatsapp_clone.routes import router as whatsapp_router
from exam_hub.routes import router as exam_hub_router
from ai_agent_browser.routes import router as ai_agent_browser_router
from ai_browser.routes import router as ai_browser_router

app = FastAPI(title="Multi-Backend Python Services")

# Configure CORS
origins = [
    "*",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
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
app.include_router(whatsapp_router)
app.include_router(exam_hub_router)
app.include_router(ai_agent_browser_router)
app.include_router(ai_browser_router)

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Multi-Backend Python Services"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 9002))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)


