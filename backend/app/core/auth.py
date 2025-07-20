"""
Authentication utilities for COGENT backend.
JWT token management and user authentication logic.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import uuid

from fastapi import HTTPException, status, Cookie, Response
from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class TokenData(BaseModel):
    """JWT token payload structure"""
    user_id: str
    email: str
    exp: int
    iat: int
    jti: str
    type: str  # "access" or "refresh"


class JWTManager:
    """JWT token creation and validation"""
    
    def __init__(self):
        self.settings = get_settings()
    
    def create_access_token(self, user_id: str, email: str) -> str:
        """Create access token with 15 minute expiry"""
        now = datetime.utcnow()
        expires = now + timedelta(minutes=self.settings.access_token_expire_minutes)
        
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": int(expires.timestamp()),
            "iat": int(now.timestamp()),
            "jti": str(uuid.uuid4()),
            "type": "access"
        }
        
        token = jwt.encode(
            payload, 
            self.settings.jwt_secret_key, 
            algorithm=self.settings.jwt_algorithm
        )
        
        logger.info(f"Created access token for user {user_id}", extra={
            "user_id": user_id,
            "expires_at": expires.isoformat(),
            "token_type": "access"
        })
        
        return token
    
    def create_refresh_token(self, user_id: str, email: str) -> str:
        """Create refresh token with 7 day expiry"""
        now = datetime.utcnow()
        expires = now + timedelta(days=self.settings.refresh_token_expire_days)
        
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": int(expires.timestamp()),
            "iat": int(now.timestamp()),
            "jti": str(uuid.uuid4()),
            "type": "refresh"
        }
        
        token = jwt.encode(
            payload,
            self.settings.jwt_secret_key,
            algorithm=self.settings.jwt_algorithm
        )
        
        logger.info(f"Created refresh token for user {user_id}", extra={
            "user_id": user_id,
            "expires_at": expires.isoformat(),
            "token_type": "refresh"
        })
        
        return token
    
    def verify_token(self, token: str, expected_type: str = "access") -> Optional[TokenData]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token,
                self.settings.jwt_secret_key,
                algorithms=[self.settings.jwt_algorithm]
            )
            
            # Validate token type
            token_type = payload.get("type")
            if token_type != expected_type:
                logger.warning(f"Invalid token type: expected {expected_type}, got {token_type}")
                return None
            
            # Validate required fields
            user_id = payload.get("user_id")
            email = payload.get("email")
            exp = payload.get("exp")
            iat = payload.get("iat")
            jti = payload.get("jti")
            
            if not all([user_id, email, exp, iat, jti]):
                logger.warning("Token missing required fields")
                return None
            
            return TokenData(
                user_id=user_id,
                email=email,
                exp=exp,
                iat=iat,
                jti=jti,
                type=token_type
            )
            
        except JWTError as e:
            logger.warning(f"JWT validation error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error validating token: {e}")
            return None
    
    def set_auth_cookies(self, response: Response, access_token: str, refresh_token: str):
        """Set authentication cookies on response"""
        settings = self.settings
        
        # Access token cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=settings.access_token_expire_minutes * 60,
            path="/api/v1",
            httponly=True,
            secure=settings.cookie_secure,
            samesite="lax",
            domain=settings.cookie_domain
        )
        
        # Refresh token cookie  
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
            path="/api/v1",
            httponly=True,
            secure=settings.cookie_secure,
            samesite="lax",
            domain=settings.cookie_domain
        )
        
        logger.info("Set authentication cookies")
    
    def clear_auth_cookies(self, response: Response):
        """Clear authentication cookies"""
        settings = self.settings
        
        response.set_cookie(
            key="access_token",
            value="",
            max_age=0,
            path="/api/v1",
            httponly=True,
            secure=settings.cookie_secure,
            samesite="lax",
            domain=settings.cookie_domain
        )
        
        response.set_cookie(
            key="refresh_token", 
            value="",
            max_age=0,
            path="/api/v1",
            httponly=True,
            secure=settings.cookie_secure,
            samesite="lax",
            domain=settings.cookie_domain
        )
        
        logger.info("Cleared authentication cookies")


# Global JWT manager instance
jwt_manager = JWTManager()


def get_current_user(access_token: Optional[str] = Cookie(None)) -> TokenData:
    """
    FastAPI dependency to get current authenticated user from access token cookie.
    Raises HTTPException if user is not authenticated.
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated - no access token provided"
        )
    
    token_data = jwt_manager.verify_token(access_token, "access")
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token"
        )
    
    logger.debug(f"Authenticated user: {token_data.user_id}")
    return token_data


def get_current_user_optional(access_token: Optional[str] = Cookie(None)) -> Optional[TokenData]:
    """
    FastAPI dependency to get current user if authenticated, None otherwise.
    Does not raise exceptions for unauthenticated requests.
    """
    if not access_token:
        return None
    
    token_data = jwt_manager.verify_token(access_token, "access") 
    if token_data:
        logger.debug(f"Authenticated user: {token_data.user_id}")
    
    return token_data


# Mock user data for authentication (using mock_data.py users)
MOCK_USERS = {
    # These will be populated from mock_data.py in actual implementation
    "test@example.com": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "test@example.com", 
        "name": "Test User",
        "github_id": "123456",
        "google_id": None,
    }
}


def mock_oauth_login(provider: str, code: str) -> Optional[Dict[str, Any]]:
    """
    Mock OAuth login implementation for development.
    In production, this would make actual OAuth calls to GitHub/Google.
    """
    logger.info(f"Mock OAuth login attempt: provider={provider}, code={code[:10]}...")
    
    # For mock implementation, accept any code and return test user
    if provider in ["github", "google"] and code:
        # Return mock user data
        user = MOCK_USERS["test@example.com"].copy()
        logger.info(f"Mock OAuth login successful for user: {user['id']}")
        return user
    
    logger.warning(f"Mock OAuth login failed: invalid provider or code")
    return None