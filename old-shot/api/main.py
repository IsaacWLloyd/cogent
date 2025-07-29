"""
FastAPI application entry point for Vercel
Single function that handles all API routes
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys

# Add shared module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from shared.models import ApiError

# Create FastAPI app
app = FastAPI(
    title="COGENT API",
    description="Code Organization and Generation Enhancement Tool",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ApiError(
            error="internal_server_error",
            message="An unexpected error occurred",
            details={"type": type(exc).__name__} if os.getenv("DEBUG") else None
        ).model_dump()
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
        "version": "1.0.0",
        "docs": "/api/docs"
    }

# Import and register routers
from routers import waitlist
# TODO: Import other routers when implemented
# from routers import auth, projects, documents, search, users, github

app.include_router(waitlist.router, prefix="/api/v1/waitlist", tags=["Waitlist"])
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
# app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
# app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
# app.include_router(search.router, prefix="/api/v1/search", tags=["Search"])
# app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
# app.include_router(github.router, prefix="/api/v1/github", tags=["GitHub"])

# Webhook endpoints
@app.post("/api/webhooks/clerk")
async def clerk_webhook(request: Request):
    """Handle Clerk user lifecycle webhooks"""
    # TODO: Implement Clerk webhook handling
    return {"status": "received"}

# Vercel serverless function handler
def handler(request, context):
    """Vercel serverless function entry point"""
    return app(request, context)

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)