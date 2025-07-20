"""
Main entry point for COGENT backend API.
Run with: uvicorn main:app --reload
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)