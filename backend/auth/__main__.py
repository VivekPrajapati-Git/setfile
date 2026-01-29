import uvicorn
import os
import sys

# Ensure the parent directory is in sys.path so 'auth' module can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    # We use "auth.main:app" string to let uvicorn handle the import and reloading
    uvicorn.run("auth.main:app", host="127.0.0.1", port=8000, reload=True)
