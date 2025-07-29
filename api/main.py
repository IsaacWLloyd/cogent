"""
Simple FastAPI application for COGENT
Clean start with just waitlist functionality
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="COGENT API",
    description="Code Organization and Generation Enhancement Tool",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "cogent-api"}

# Root endpoint
@app.get("/api")
async def root():
    return {
        "message": "COGENT API",
        "version": "1.0.0"
    }

# Import and register waitlist router
from waitlist import router as waitlist_router
app.include_router(waitlist_router, prefix="/api/v1", tags=["Waitlist"])

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)