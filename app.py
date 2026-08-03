import os
import sys

# Get the directory where app.py is located
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

# If main.py is not in current directory, check subdirectories (e.g. if git cloned into python-backend folder)
if not os.path.exists(os.path.join(base_dir, "main.py")):
    for item in os.listdir(base_dir):
        sub_dir = os.path.join(base_dir, item)
        if os.path.isdir(sub_dir) and os.path.exists(os.path.join(sub_dir, "main.py")):
            sys.path.insert(0, sub_dir)
            os.chdir(sub_dir)
            print(f"Found main.py in subdirectory: {sub_dir}")
            break

import uvicorn
from main import app

if __name__ == "__main__":
    port = int(os.getenv("PORT") or os.getenv("SERVER_PORT") or 9002)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
