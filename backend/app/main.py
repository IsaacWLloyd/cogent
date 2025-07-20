"""
FastAPI application factory and main application setup for COGENT backend.
"""

import uuid
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.database import init_db
from app.core.logging_config import setup_logging
from app.routers import auth, projects, documents, search, users


# Global request correlation tracking
request_context: Dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    settings = get_settings()
    setup_logging()
    
    logger = logging.getLogger(__name__)
    logger.info("Starting COGENT Backend API")
    
    # Initialize database
    await init_db()
    logger.info(f"Database initialized with URL: {settings.database_url}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down COGENT Backend API")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    settings = get_settings()
    
    app = FastAPI(
        title="COGENT API",
        description="API for Code Organization and Generation Enhancement Tool",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.environment == "development" else None,
        redoc_url="/redoc" if settings.environment == "development" else None,
    )
    
    # Add middleware
    _setup_middleware(app, settings)
    
    # Add custom middleware for request logging and correlation IDs
    @app.middleware("http")
    async def logging_middleware(request: Request, call_next):
        # Generate correlation ID for request tracking
        correlation_id = str(uuid.uuid4())
        request_context["correlation_id"] = correlation_id
        
        # Log incoming request
        start_time = datetime.utcnow()
        logger = logging.getLogger(__name__)
        logger.info(
            f"Request started",
            extra={
                "correlation_id": correlation_id,
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
            }
        )
        
        # Process request
        response = await call_next(request)
        
        # Log response
        end_time = datetime.utcnow()
        duration_ms = (end_time - start_time).total_seconds() * 1000
        
        logger.info(
            f"Request completed",
            extra={
                "correlation_id": correlation_id,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
            }
        )
        
        # Add correlation ID to response headers
        response.headers["X-Correlation-ID"] = correlation_id
        
        return response
    
    # Include routers
    _setup_routes(app)
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger = logging.getLogger(__name__)
        correlation_id = request_context.get("correlation_id", "unknown")
        
        logger.error(
            f"Unhandled exception: {exc}",
            extra={
                "correlation_id": correlation_id,
                "exception_type": type(exc).__name__,
                "url": str(request.url),
            },
            exc_info=True if settings.environment == "development" else False
        )
        
        # Return sanitized error in production
        if settings.environment == "production":
            return JSONResponse(
                status_code=500,
                content={
                    "data": None,
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": "An internal server error occurred"
                    },
                    "meta": {
                        "correlationId": correlation_id,
                        "timestamp": datetime.utcnow().isoformat(),
                        "apiVersion": "1.0.0"
                    }
                }
            )
        else:
            # Development: include full error details
            return JSONResponse(
                status_code=500,
                content={
                    "data": None,
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": str(exc),
                        "type": type(exc).__name__
                    },
                    "meta": {
                        "correlationId": correlation_id,
                        "timestamp": datetime.utcnow().isoformat(),
                        "apiVersion": "1.0.0"
                    }
                }
            )
    
    return app


def _setup_middleware(app: FastAPI, settings):
    """Configure application middleware"""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware for production
    if settings.environment == "production":
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.allowed_hosts
        )


def _setup_routes(app: FastAPI):
    """Configure application routes"""
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {
            "data": {
                "status": "healthy",
                "service": "cogent-backend",
                "version": "1.0.0"
            },
            "error": None,
            "meta": {
                "timestamp": datetime.utcnow().isoformat(),
                "apiVersion": "1.0.0"
            }
        }
    
    # API v1 routes
    API_PREFIX = "/api/v1"
    
    app.include_router(auth.router, prefix=API_PREFIX, tags=["Authentication"])
    app.include_router(projects.router, prefix=API_PREFIX, tags=["Projects"])
    app.include_router(documents.router, prefix=API_PREFIX, tags=["Documents"])
    app.include_router(search.router, prefix=API_PREFIX, tags=["Search"])
    app.include_router(users.router, prefix=API_PREFIX, tags=["User"])


# Create the application instance
app = create_app()