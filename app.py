import os
import sys
import shutil
import subprocess

# Get the base directory (/home/container)
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

# Check if main.py exists in base_dir or any subfolder
main_exists = os.path.exists(os.path.join(base_dir, "main.py"))

if not main_exists:
    # Check if main.py is inside a subdirectory
    for item in os.listdir(base_dir):
        sub_dir = os.path.join(base_dir, item)
        if os.path.isdir(sub_dir) and os.path.exists(os.path.join(sub_dir, "main.py")):
            sys.path.insert(0, sub_dir)
            os.chdir(sub_dir)
            base_dir = sub_dir
            main_exists = True
            print(f"--> Found main.py in subdirectory: {sub_dir}")
            break

if not main_exists:
    print("--> main.py not found in /home/container. Auto-cloning repository from GitHub...")
    repo_url = "https://github.com/Dilmith-Ranasinghe518/python-backend.git"
    tmp_clone_dir = "/tmp/python-backend-clone"
    
    try:
        if os.path.exists(tmp_clone_dir):
            shutil.rmtree(tmp_clone_dir)
        
        # Clone repository to temp folder
        subprocess.run(["git", "clone", repo_url, tmp_clone_dir], check=True)
        
        # Copy all contents from temp folder to base_dir (/home/container)
        for item in os.listdir(tmp_clone_dir):
            src = os.path.join(tmp_clone_dir, item)
            dst = os.path.join(base_dir, item)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        
        shutil.rmtree(tmp_clone_dir)
        print("--> Repository files and .git cloned successfully!")
    except Exception as e:
        print(f"--> Failed to auto-clone repository: {e}")

import uvicorn
from main import app

if __name__ == "__main__":
    port = int(os.getenv("PORT") or os.getenv("SERVER_PORT") or 9002)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
