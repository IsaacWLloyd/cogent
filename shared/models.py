"""
Shared Python types for COGENT using Pydantic
These types match the OpenAPI specification and can be used across backend and MCP server
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, EmailStr, HttpUrl
import uuid


# User models
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    github_id: Optional[str] = Field(None, alias="githubId")
    google_id: Optional[str] = Field(None, alias="googleId")

    class Config:
        populate_by_name = True


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None


class User(UserBase):
    id: uuid.UUID
    created_at: datetime = Field(alias="createdAt")

    class Config:
        from_attributes = True
        populate_by_name = True


# Project models
class ProjectBase(BaseModel):
    name: str
    repo_url: Optional[HttpUrl] = Field(None, alias="repoUrl")

    class Config:
        populate_by_name = True


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    repo_url: Optional[HttpUrl] = Field(None, alias="repoUrl")

    class Config:
        populate_by_name = True


class Project(ProjectBase):
    id: uuid.UUID
    user_id: uuid.UUID = Field(alias="userId")
    api_key: str = Field(alias="apiKey")
    created_at: datetime = Field(alias="createdAt")

    class Config:
        from_attributes = True
        populate_by_name = True


# Document models
class DocumentBase(BaseModel):
    file_path: str = Field(alias="filePath")
    content: str
    summary: str

    class Config:
        populate_by_name = True


class DocumentCreate(DocumentBase):
    pass


class Document(DocumentBase):
    id: uuid.UUID
    project_id: uuid.UUID = Field(alias="projectId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        from_attributes = True
        populate_by_name = True


# Search models
class SearchRequest(BaseModel):
    query: str
    limit: int = Field(10, ge=1, le=50)
    offset: int = Field(0, ge=0)


class SearchResult(BaseModel):
    document_id: uuid.UUID = Field(alias="documentId")
    file_path: str = Field(alias="filePath")
    content: str  # Relevant excerpt
    relevance_score: float = Field(ge=0, le=1, alias="relevanceScore")

    class Config:
        populate_by_name = True


class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int
    query: str


# Auth models
AuthProvider = Literal["github", "google"]


class LoginRequest(BaseModel):
    provider: AuthProvider
    code: str


class LoginResponse(BaseModel):
    user: User
    expires_at: datetime = Field(alias="expiresAt")

    class Config:
        populate_by_name = True


class RefreshResponse(BaseModel):
    expires_at: datetime = Field(alias="expiresAt")

    class Config:
        populate_by_name = True


# Pagination models
class PaginatedResponse(BaseModel):
    total: int
    limit: int
    offset: int


class ProjectsResponse(PaginatedResponse):
    projects: List[Project]


class DocumentsResponse(PaginatedResponse):
    documents: List[Document]


# Usage models
class DailyUsage(BaseModel):
    date: str  # ISO date string
    tokens: int
    cost: float


class UsageStats(BaseModel):
    total_tokens: int = Field(alias="totalTokens")
    total_cost: float = Field(alias="totalCost")
    documents_generated: int = Field(alias="documentsGenerated")
    searches_performed: int = Field(alias="searchesPerformed")
    daily_usage: Optional[List[DailyUsage]] = Field(None, alias="dailyUsage")

    class Config:
        populate_by_name = True


# Error model
class ApiError(BaseModel):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None


# MCP-specific models
class DocumentContext(BaseModel):
    """Document context for MCP server"""
    project_id: uuid.UUID
    file_path: str
    content: str
    summary: str
    relevance_score: Optional[float] = None


class ContextRequest(BaseModel):
    """Request for context retrieval from MCP server"""
    project_id: uuid.UUID
    query: str
    max_results: int = Field(10, ge=1, le=50)


class ContextResponse(BaseModel):
    """Response with relevant context from MCP server"""
    contexts: List[DocumentContext]
    total_found: int