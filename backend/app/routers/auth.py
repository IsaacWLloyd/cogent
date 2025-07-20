"""
Authentication router for COGENT API.
Handles OAuth login, logout, and token refresh.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, status, Response, Cookie, Depends
from pydantic import BaseModel

from app.core.auth import jwt_manager, mock_oauth_login, get_current_user
from app.core.responses import success_response, error_response, unauthorized_error_response
from shared.models import LoginRequest, User

logger = logging.getLogger(__name__)

router = APIRouter()


class LoginResponse(BaseModel):
    """Login response with user data and token expiration"""
    user: User
    expiresAt: datetime


class RefreshResponse(BaseModel):
    """Token refresh response"""
    expiresAt: datetime


@router.post("/auth/login")
async def login(request: LoginRequest, response: Response):
    """
    OAuth login endpoint.
    Mock implementation that accepts any valid provider/code and returns test user.
    """
    logger.info(f"Login attempt: provider={request.provider}")
    
    try:
        # Mock OAuth exchange - in production this would call actual OAuth APIs
        user_data = mock_oauth_login(request.provider, request.code)
        
        if not user_data:
            logger.warning(f"OAuth login failed for provider: {request.provider}")
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=unauthorized_error_response("Invalid OAuth code or provider")
            )
        
        # Create JWT tokens
        access_token = jwt_manager.create_access_token(
            user_id=user_data["id"],
            email=user_data["email"]
        )
        
        refresh_token = jwt_manager.create_refresh_token(
            user_id=user_data["id"], 
            email=user_data["email"]
        )
        
        # Set authentication cookies
        jwt_manager.set_auth_cookies(response, access_token, refresh_token)
        
        # Create user response object
        user = User(
            id=user_data["id"],
            email=user_data["email"],
            name=user_data.get("name"),
            githubId=user_data.get("github_id"),
            googleId=user_data.get("google_id"),
            createdAt=datetime.utcnow()  # Mock created date
        )
        
        # Calculate token expiration
        expires_at = datetime.utcnow() + timedelta(
            minutes=jwt_manager.settings.access_token_expire_minutes
        )
        
        login_response = LoginResponse(
            user=user,
            expiresAt=expires_at
        )
        
        logger.info(f"User logged in successfully: {user_data['id']}")
        
        return success_response(login_response.dict())
        
    except Exception as e:
        logger.error(f"Login error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_ERROR", "Login failed")
        )


@router.post("/auth/logout")
async def logout(response: Response):
    """
    Logout endpoint - clears authentication cookies.
    """
    logger.info("User logout")
    
    try:
        # Clear authentication cookies
        jwt_manager.clear_auth_cookies(response)
        
        logger.info("User logged out successfully")
        
        return success_response({"message": "Logged out successfully"})
        
    except Exception as e:
        logger.error(f"Logout error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_ERROR", "Logout failed")
        )


@router.post("/auth/refresh")
async def refresh_token(
    response: Response,
    refresh_token: Optional[str] = Cookie(None)
):
    """
    Token refresh endpoint.
    Uses refresh token to generate new access token.
    """
    logger.info("Token refresh attempt")
    
    try:
        if not refresh_token:
            logger.warning("Token refresh failed: no refresh token provided")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=unauthorized_error_response("No refresh token provided")
            )
        
        # Verify refresh token
        token_data = jwt_manager.verify_token(refresh_token, "refresh")
        if not token_data:
            logger.warning("Token refresh failed: invalid refresh token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=unauthorized_error_response("Invalid or expired refresh token")
            )
        
        # Create new access token
        new_access_token = jwt_manager.create_access_token(
            user_id=token_data.user_id,
            email=token_data.email
        )
        
        # Set new access token cookie (keep existing refresh token)
        settings = jwt_manager.settings
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            max_age=settings.access_token_expire_minutes * 60,
            path="/api/v1",
            httponly=True,
            secure=settings.cookie_secure,
            samesite="lax",
            domain=settings.cookie_domain
        )
        
        # Calculate new expiration
        expires_at = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        
        refresh_response = RefreshResponse(expiresAt=expires_at)
        
        logger.info(f"Token refreshed successfully for user: {token_data.user_id}")
        
        return success_response(refresh_response.dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_ERROR", "Token refresh failed")
        )