import os
import uvicorn
from main import app

if __name__ == "__main__":
    # Fetch port from PORT or SERVER_PORT (commonly set by hosting panels like Pterodactyl)
    port = int(os.getenv("PORT") or os.getenv("SERVER_PORT") or 9002)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
