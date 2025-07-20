"""
Tests for authentication endpoints.
"""

import pytest
from fastapi import status


def test_login_success(client):
    """Test successful OAuth login"""
    response = client.post("/api/v1/auth/login", json={
        "provider": "github",
        "code": "test_code_123"
    })
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"] is not None
    assert "user" in data["data"]
    assert "expiresAt" in data["data"]
    assert data["error"] is None
    
    # Check cookies are set
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


def test_login_invalid_provider(client):
    """Test login with invalid provider"""
    response = client.post("/api/v1/auth/login", json={
        "provider": "invalid",
        "code": "test_code"
    })
    
    # Should return validation error due to enum constraint
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_logout(client):
    """Test logout endpoint"""
    response = client.post("/api/v1/auth/logout")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"] is not None
    assert data["error"] is None
    
    # Check cookies are cleared (they will be in the response headers)
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


def test_refresh_token_missing(client):
    """Test refresh without refresh token"""
    response = client.post("/api/v1/auth/refresh")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED