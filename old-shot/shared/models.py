"""
Shared Python types for COGENT using Pydantic
These types match the OpenAPI specification and SQLAlchemy models
Updated to match SPRINT0_SPEC.md Extended Schema
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Literal, Union
from pydantic import BaseModel, Field, EmailStr, HttpUrl, ConfigDict
from enum import Enum
import uuid


# Enums
class VisibilityEnum(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"


class OperationTypeEnum(str, Enum):
    SEARCH = "search"
    GENERATE = "generate"
    MCP_CALL = "mcp_call"


class SearchTypeEnum(str, Enum):
    FULL_TEXT = "full_text"
    SEMANTIC = "semantic"
    HYBRID = "hybrid"


# Base models with common patterns
class TimestampedModel(BaseModel):
    created_at: datetime
    updated_at: datetime


# User models
class UserBase(BaseModel):
    clerk_id: str
    email: EmailStr
    name: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    settings_json: Optional[Dict[str, Any]] = None


class User(UserBase, TimestampedModel):
    id: uuid.UUID
    settings_json: Optional[Dict[str, Any]] = None
    clerk_org_id: Optional[str] = None
    last_seen: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Project models
class ProjectBase(BaseModel):
    name: str
    github_repo_url: HttpUrl
    description: Optional[str] = None
    visibility: VisibilityEnum = VisibilityEnum.PRIVATE
    branch_name: str = "main"
    include_patterns: List[str] = ["**/*"]
    exclude_patterns: List[str] = ["node_modules/**", ".git/**"]


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[VisibilityEnum] = None
    settings_json: Optional[Dict[str, Any]] = None
    branch_name: Optional[str] = None
    include_patterns: Optional[List[str]] = None
    exclude_patterns: Optional[List[str]] = None


class Project(ProjectBase, TimestampedModel):
    id: uuid.UUID
    user_id: uuid.UUID
    settings_json: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


# Document models
class DocumentBase(BaseModel):
    file_path: str
    content: str
    summary: str
    commit_hash: str
    language: Optional[str] = None
    imports: Optional[List[str]] = None
    exports: Optional[List[str]] = None
    references: Optional[List[str]] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    content: Optional[str] = None
    summary: Optional[str] = None
    commit_hash: Optional[str] = None
    language: Optional[str] = None
    imports: Optional[List[str]] = None
    exports: Optional[List[str]] = None
    references: Optional[List[str]] = None


class Document(DocumentBase, TimestampedModel):
    id: uuid.UUID
    project_id: uuid.UUID
    version: int = 1

    model_config = ConfigDict(from_attributes=True)


# API Key models
class ApiKeyBase(BaseModel):
    name: str


class ApiKeyCreate(ApiKeyBase):
    pass


class ApiKey(ApiKeyBase):
    id: uuid.UUID
    project_id: uuid.UUID
    created_at: datetime
    last_used: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ApiKeyCreateResponse(BaseModel):
    api_key: ApiKey
    key: str  # Only returned once upon creation


# Usage models
class UsageBase(BaseModel):
    operation_type: OperationTypeEnum
    tokens_used: int = Field(ge=0)
    cost: float = Field(ge=0)
    llm_model: str
    endpoint_called: str
    response_time: Optional[int] = None


class UsageCreate(UsageBase):
    project_id: uuid.UUID


class Usage(UsageBase):
    id: uuid.UUID
    project_id: uuid.UUID
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


# Search models
class SearchFilters(BaseModel):
    language: Optional[str] = None
    file_patterns: Optional[List[str]] = None
    date_range: Optional[Dict[str, datetime]] = None


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    search_type: SearchTypeEnum = SearchTypeEnum.HYBRID
    max_results: int = Field(10, ge=1, le=50)
    filters: Optional[SearchFilters] = None


class SearchResult(BaseModel):
    document: Document
    score: float = Field(ge=0, le=1)
    highlights: List[str] = []


class SearchResponse(BaseModel):
    results: List[SearchResult]
    total_results: int
    search_time_ms: int


# Clerk integration models
class ClerkEmailAddress(BaseModel):
    email_address: EmailStr
    id: str


class ClerkUser(BaseModel):
    id: str
    email_addresses: List[ClerkEmailAddress]
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: int
    updated_at: int


class ClerkWebhook(BaseModel):
    type: Literal["user.created", "user.updated", "user.deleted"]
    data: ClerkUser


# GitHub integration models
class GitHubPermissions(BaseModel):
    admin: bool
    push: bool
    pull: bool


class GitHubRepository(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    html_url: HttpUrl
    description: Optional[str] = None
    default_branch: str
    permissions: GitHubPermissions


class GitHubFile(BaseModel):
    name: str
    path: str
    sha: str
    size: int
    type: Literal["file", "dir"]
    content: Optional[str] = None
    encoding: Optional[str] = None


class GitHubFileUpdate(BaseModel):
    path: str
    content: str
    message: str
    branch: str = "main"
    sha: Optional[str] = None


# Response models
class PaginatedResponse(BaseModel):
    total: int
    limit: int
    offset: int


class ProjectsResponse(PaginatedResponse):
    projects: List[Project]


class DocumentsResponse(BaseModel):
    documents: List[Document]
    total: int


class ApiKeysResponse(BaseModel):
    api_keys: List[ApiKey]


class UsageStatsResponse(BaseModel):
    total_operations: int
    total_tokens: int
    total_cost: float
    operations_by_type: Dict[str, int]
    daily_usage: List[Dict[str, Union[str, int, float]]]


class GitHubReposResponse(BaseModel):
    repositories: List[GitHubRepository]


class GitHubFilesResponse(BaseModel):
    files: List[GitHubFile]


# Error models
class ApiError(BaseModel):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None


# MCP Server models
class DocumentContext(BaseModel):
    project_id: uuid.UUID
    file_path: str
    content: str
    summary: str
    relevance_score: Optional[float] = None


class ContextRequest(BaseModel):
    project_id: uuid.UUID
    query: str
    max_results: int = Field(10, ge=1, le=50)


class ContextResponse(BaseModel):
    contexts: List[DocumentContext]
    total_found: int


# Utility functions
def get_language_from_path(file_path: str) -> Optional[str]:
    """Extract programming language from file path"""
    language_map = {
        '.js': 'javascript',
        '.jsx': 'javascript', 
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.py': 'python',
        '.java': 'java',
        '.go': 'go',
        '.rs': 'rust',
        '.cpp': 'cpp',
        '.c': 'c',
        '.cs': 'csharp',
        '.php': 'php',
        '.rb': 'ruby',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.scala': 'scala',
        '.sh': 'bash',
        '.sql': 'sql',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.md': 'markdown',
        '.html': 'html',
        '.css': 'css',
        '.vue': 'vue',
        '.svelte': 'svelte',
    }
    
    ext = file_path.lower().split('.')[-1]
    return language_map.get(f'.{ext}')


# Export commonly used models
__all__ = [
    # Enums
    'VisibilityEnum',
    'OperationTypeEnum', 
    'SearchTypeEnum',
    # User models
    'User',
    'UserCreate',
    'UserUpdate',
    # Project models
    'Project',
    'ProjectCreate',
    'ProjectUpdate',
    # Document models
    'Document',
    'DocumentCreate',
    'DocumentUpdate',
    # API Key models
    'ApiKey',
    'ApiKeyCreate',
    'ApiKeyCreateResponse',
    # Usage models
    'Usage',
    'UsageCreate',
    # Search models
    'SearchRequest',
    'SearchResponse',
    'SearchResult',
    # Clerk models
    'ClerkUser',
    'ClerkWebhook',
    # GitHub models
    'GitHubRepository',
    'GitHubFile',
    'GitHubFileUpdate',
    # Response models
    'ProjectsResponse',
    'DocumentsResponse',
    'ApiKeysResponse',
    'UsageStatsResponse',
    'GitHubReposResponse',
    'GitHubFilesResponse',
    # Error models
    'ApiError',
    # MCP models
    'DocumentContext',
    'ContextRequest',
    'ContextResponse',
    # Utilities
    'get_language_from_path',
]