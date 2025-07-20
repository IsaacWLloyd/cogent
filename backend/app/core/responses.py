"""
Standardized response formats for COGENT API.
Implements consistent response envelope with metadata.
"""

from datetime import datetime
from typing import Any, Optional, Dict
from pydantic import BaseModel

from app.core.config import get_settings


class ApiResponse(BaseModel):
    """Standard API response envelope"""
    data: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    meta: Dict[str, Any]


class ErrorDetail(BaseModel):
    """Error details structure"""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


def create_response(
    data: Any = None,
    error: Optional[ErrorDetail] = None,
    correlation_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create standardized API response with metadata.
    
    Args:
        data: Response data (None for error responses)
        error: Error details (None for success responses)
        correlation_id: Request correlation ID for tracking
    
    Returns:
        Standardized response dictionary
    """
    # Import here to avoid circular imports
    from app.main import request_context
    
    if correlation_id is None:
        correlation_id = request_context.get("correlation_id", "unknown")
    
    response = {
        "data": data,
        "error": error.dict() if error else None,
        "meta": {
            "correlationId": correlation_id,
            "timestamp": datetime.utcnow().isoformat(),
            "apiVersion": "1.0.0"
        }
    }
    
    return response


def success_response(data: Any, correlation_id: Optional[str] = None) -> Dict[str, Any]:
    """Create success response"""
    return create_response(data=data, correlation_id=correlation_id)


def error_response(
    code: str,
    message: str, 
    details: Optional[Dict[str, Any]] = None,
    correlation_id: Optional[str] = None
) -> Dict[str, Any]:
    """Create error response"""
    error = ErrorDetail(code=code, message=message, details=details)
    return create_response(error=error, correlation_id=correlation_id)


# Common error responses
def validation_error_response(details: Dict[str, Any]) -> Dict[str, Any]:
    """422 Validation Error"""
    return error_response(
        code="VALIDATION_ERROR",
        message="Request validation failed",
        details=details
    )


def unauthorized_error_response(message: str = "Authentication required") -> Dict[str, Any]:
    """401 Unauthorized Error"""
    return error_response(
        code="UNAUTHORIZED",
        message=message
    )


def forbidden_error_response(message: str = "Access forbidden") -> Dict[str, Any]:
    """403 Forbidden Error"""
    return error_response(
        code="FORBIDDEN", 
        message=message
    )


def not_found_error_response(resource: str) -> Dict[str, Any]:
    """404 Not Found Error"""
    return error_response(
        code="NOT_FOUND",
        message=f"{resource} not found"
    )


def conflict_error_response(message: str) -> Dict[str, Any]:
    """409 Conflict Error"""
    return error_response(
        code="CONFLICT",
        message=message
    )


def rate_limit_error_response() -> Dict[str, Any]:
    """429 Rate Limit Error"""
    return error_response(
        code="RATE_LIMIT_EXCEEDED",
        message="Too many requests, please try again later"
    )