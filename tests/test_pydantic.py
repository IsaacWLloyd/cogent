"""
Pydantic model validation tests for COGENT
Tests all API request/response models and data validation
"""

import pytest
from pydantic import ValidationError
from datetime import datetime
from uuid import uuid4

# Add shared module to path
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from shared.models import (
    # User models
    User, UserCreate, UserUpdate,
    
    # Project models
    Project, ProjectCreate, ProjectUpdate,
    
    # Document models
    Document, DocumentCreate, DocumentUpdate,
    
    # API Key models
    ApiKey, ApiKeyCreate, ApiKeyCreateResponse,
    
    # Usage models
    Usage, UsageCreate,
    
    # Search models
    SearchRequest, SearchResponse, SearchResult, SearchFilters,
    
    # Clerk models
    ClerkUser, ClerkWebhook, ClerkEmailAddress,
    
    # GitHub models
    GitHubRepository, GitHubFile, GitHubFileUpdate, GitHubPermissions,
    
    # Response models
    ProjectsResponse, DocumentsResponse, ApiKeysResponse,
    UsageStatsResponse, GitHubReposResponse, GitHubFilesResponse,
    
    # Error and MCP models
    ApiError, DocumentContext, ContextRequest, ContextResponse,
    
    # Enums
    VisibilityEnum, OperationTypeEnum, SearchTypeEnum,
    
    # Utility functions
    get_language_from_path
)


class TestUserModels:
    """Test User-related Pydantic models"""
    
    def test_user_create_valid(self):
        """Test valid UserCreate model"""
        user_data = {
            "clerk_id": "user_clerk_123",
            "email": "test@example.com",
            "name": "Test User"
        }
        user = UserCreate(**user_data)
        assert user.clerk_id == "user_clerk_123"
        assert user.email == "test@example.com"
        assert user.name == "Test User"
    
    def test_user_create_invalid_email(self):
        """Test UserCreate with invalid email"""
        user_data = {
            "clerk_id": "user_clerk_123",
            "email": "invalid-email",  # Invalid email format
            "name": "Test User"
        }
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)
        
        assert "email" in str(exc_info.value)
    
    def test_user_update_optional_fields(self):
        """Test UserUpdate with optional fields"""
        # Empty update
        update1 = UserUpdate()
        assert update1.name is None
        assert update1.settings_json is None
        
        # Partial update
        update2 = UserUpdate(name="Updated Name")
        assert update2.name == "Updated Name"
        assert update2.settings_json is None
        
        # Full update
        settings = {"theme": "dark", "notifications": False}
        update3 = UserUpdate(name="New Name", settings_json=settings)
        assert update3.name == "New Name"
        assert update3.settings_json == settings
    
    def test_user_model_serialization(self):
        """Test User model serialization"""
        user_data = {
            "id": uuid4(),
            "clerk_id": "user_clerk_456",
            "email": "serialize@example.com",
            "name": "Serialize User",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "settings_json": {"theme": "light"},
            "clerk_org_id": "org_123",
            "last_seen": datetime.now()
        }
        user = User(**user_data)
        
        # Test model_dump (serialization)
        serialized = user.model_dump()
        assert serialized["clerk_id"] == "user_clerk_456"
        assert serialized["email"] == "serialize@example.com"
        assert "settings_json" in serialized


class TestProjectModels:
    """Test Project-related Pydantic models"""
    
    def test_project_create_valid(self):
        """Test valid ProjectCreate model"""
        project_data = {
            "name": "Test Project",
            "github_repo_url": "https://github.com/user/repo",
            "description": "A test project",
            "visibility": VisibilityEnum.PRIVATE,
            "branch_name": "main",
            "include_patterns": ["**/*.py", "**/*.js"],
            "exclude_patterns": ["node_modules/**", "__pycache__/**"]
        }
        project = ProjectCreate(**project_data)
        assert project.name == "Test Project"
        assert str(project.github_repo_url) == "https://github.com/user/repo"
        assert project.visibility == VisibilityEnum.PRIVATE
        assert project.branch_name == "main"
    
    def test_project_create_minimal(self):
        """Test ProjectCreate with minimal required fields"""
        project_data = {
            "name": "Minimal Project",
            "github_repo_url": "https://github.com/user/minimal"
        }
        project = ProjectCreate(**project_data)
        assert project.name == "Minimal Project"
        assert project.visibility == VisibilityEnum.PRIVATE  # default
        assert project.branch_name == "main"  # default
        assert project.include_patterns == ["**/*"]  # default
    
    def test_project_create_invalid_url(self):
        """Test ProjectCreate with invalid GitHub URL"""
        project_data = {
            "name": "Invalid URL Project",
            "github_repo_url": "not-a-valid-url"
        }
        with pytest.raises(ValidationError) as exc_info:
            ProjectCreate(**project_data)
        
        assert "github_repo_url" in str(exc_info.value)
    
    def test_project_update_partial(self):
        """Test ProjectUpdate with partial updates"""
        update = ProjectUpdate(
            name="Updated Name",
            visibility=VisibilityEnum.PUBLIC
        )
        assert update.name == "Updated Name"
        assert update.visibility == VisibilityEnum.PUBLIC
        assert update.description is None  # not updated
    
    def test_visibility_enum_validation(self):
        """Test VisibilityEnum validation"""
        # Valid values
        project1 = ProjectCreate(
            name="Public Project",
            github_repo_url="https://github.com/user/public",
            visibility=VisibilityEnum.PUBLIC
        )
        assert project1.visibility == VisibilityEnum.PUBLIC
        
        project2 = ProjectCreate(
            name="Private Project", 
            github_repo_url="https://github.com/user/private",
            visibility=VisibilityEnum.PRIVATE
        )
        assert project2.visibility == VisibilityEnum.PRIVATE


class TestDocumentModels:
    """Test Document-related Pydantic models"""
    
    def test_document_create_valid(self):
        """Test valid DocumentCreate model"""
        doc_data = {
            "file_path": "src/auth.py",
            "content": "def login():\n    pass",
            "summary": "Authentication module",
            "commit_hash": "abc123def456",
            "language": "python",
            "imports": ["hashlib", "jwt"],
            "exports": ["login", "logout"],
            "references": ["src/utils.py"]
        }
        document = DocumentCreate(**doc_data)
        assert document.file_path == "src/auth.py"
        assert document.language == "python"
        assert "hashlib" in document.imports
        assert "login" in document.exports
    
    def test_document_create_minimal(self):
        """Test DocumentCreate with minimal required fields"""
        doc_data = {
            "file_path": "minimal.py",
            "content": "# Minimal file",
            "summary": "Minimal document",
            "commit_hash": "minimal123"
        }
        document = DocumentCreate(**doc_data)
        assert document.file_path == "minimal.py"
        assert document.language is None  # optional
        assert document.imports is None  # optional
    
    def test_document_update_optional(self):
        """Test DocumentUpdate with optional fields"""
        update = DocumentUpdate(
            content="# Updated content",
            language="typescript"
        )
        assert update.content == "# Updated content"
        assert update.language == "typescript"
        assert update.summary is None  # not updated


class TestSearchModels:
    """Test Search-related Pydantic models"""
    
    def test_search_request_valid(self):
        """Test valid SearchRequest model"""
        search_data = {
            "query": "authentication function",
            "search_type": SearchTypeEnum.HYBRID,
            "max_results": 15,
            "filters": {
                "language": "python",
                "file_patterns": ["**/*.py"],
                "date_range": {
                    "start": "2024-01-01T00:00:00Z",
                    "end": "2024-12-31T23:59:59Z"
                }
            }
        }
        request = SearchRequest(**search_data)
        assert request.query == "authentication function"
        assert request.search_type == SearchTypeEnum.HYBRID
        assert request.max_results == 15
        assert request.filters.language == "python"
    
    def test_search_request_minimal(self):
        """Test SearchRequest with minimal fields"""
        request = SearchRequest(query="test search")
        assert request.query == "test search"
        assert request.search_type == SearchTypeEnum.HYBRID  # default
        assert request.max_results == 10  # default
        assert request.filters is None
    
    def test_search_request_validation(self):
        """Test SearchRequest validation rules"""
        # Empty query should fail
        with pytest.raises(ValidationError):
            SearchRequest(query="")
        
        # Max results too high should fail (constrained to 50)
        with pytest.raises(ValidationError):
            SearchRequest(query="test", max_results=100)
        
        # Valid max results
        request = SearchRequest(query="test", max_results=50)
        assert request.max_results == 50
        
        # Max results too low
        with pytest.raises(ValidationError):
            SearchRequest(query="test", max_results=0)
    
    def test_search_type_enum(self):
        """Test SearchTypeEnum validation"""
        for search_type in [SearchTypeEnum.FULL_TEXT, SearchTypeEnum.SEMANTIC, SearchTypeEnum.HYBRID]:
            request = SearchRequest(query="test", search_type=search_type)
            assert request.search_type == search_type
    
    def test_search_response_model(self):
        """Test SearchResponse model"""
        # Mock document for search result
        doc_data = {
            "id": uuid4(),
            "project_id": uuid4(),
            "file_path": "test.py",
            "content": "test content",
            "summary": "test summary",
            "commit_hash": "test123",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "version": 1
        }
        document = Document(**doc_data)
        
        result = SearchResult(
            document=document,
            score=0.85,
            highlights=["test content", "summary"]
        )
        
        response = SearchResponse(
            results=[result],
            total_results=1,
            search_time_ms=150
        )
        
        assert len(response.results) == 1
        assert response.results[0].score == 0.85
        assert response.total_results == 1
        assert response.search_time_ms == 150


class TestApiKeyModels:
    """Test API Key-related Pydantic models"""
    
    def test_api_key_create(self):
        """Test ApiKeyCreate model"""
        key_data = {"name": "Production Key"}
        api_key = ApiKeyCreate(**key_data)
        assert api_key.name == "Production Key"
    
    def test_api_key_model(self):
        """Test ApiKey model"""
        key_data = {
            "id": uuid4(),
            "project_id": uuid4(),
            "name": "Test Key",
            "created_at": datetime.now(),
            "last_used": datetime.now()
        }
        api_key = ApiKey(**key_data)
        assert api_key.name == "Test Key"
        assert api_key.last_used is not None
    
    def test_api_key_create_response(self):
        """Test ApiKeyCreateResponse model"""
        key_data = {
            "id": uuid4(),
            "project_id": uuid4(),
            "name": "New Key",
            "created_at": datetime.now()
        }
        api_key = ApiKey(**key_data)
        
        response = ApiKeyCreateResponse(
            api_key=api_key,
            key="sk_test_1234567890abcdef"
        )
        assert response.api_key.name == "New Key"
        assert response.key == "sk_test_1234567890abcdef"


class TestClerkModels:
    """Test Clerk integration models"""
    
    def test_clerk_email_address(self):
        """Test ClerkEmailAddress model"""
        email_data = {
            "email_address": "test@example.com",
            "id": "email_123"
        }
        email = ClerkEmailAddress(**email_data)
        assert email.email_address == "test@example.com"
        assert email.id == "email_123"
    
    def test_clerk_user(self):
        """Test ClerkUser model"""
        user_data = {
            "id": "user_clerk_123",
            "email_addresses": [
                {"email_address": "primary@example.com", "id": "email_1"},
                {"email_address": "secondary@example.com", "id": "email_2"}
            ],
            "first_name": "John",
            "last_name": "Doe",
            "created_at": 1640995200,  # Unix timestamp
            "updated_at": 1640995200
        }
        user = ClerkUser(**user_data)
        assert user.id == "user_clerk_123"
        assert len(user.email_addresses) == 2
        assert user.first_name == "John"
        assert user.last_name == "Doe"
    
    def test_clerk_webhook(self):
        """Test ClerkWebhook model"""
        webhook_data = {
            "type": "user.created",
            "data": {
                "id": "user_new_123",
                "email_addresses": [
                    {"email_address": "new@example.com", "id": "email_new"}
                ],
                "first_name": "New",
                "last_name": "User",
                "created_at": 1640995200,
                "updated_at": 1640995200
            }
        }
        webhook = ClerkWebhook(**webhook_data)
        assert webhook.type == "user.created"
        assert webhook.data.id == "user_new_123"
        assert webhook.data.email_addresses[0].email_address == "new@example.com"
    
    def test_clerk_webhook_invalid_type(self):
        """Test ClerkWebhook with invalid event type"""
        webhook_data = {
            "type": "invalid.event",  # Invalid event type
            "data": {
                "id": "user_123",
                "email_addresses": [],
                "created_at": 1640995200,
                "updated_at": 1640995200
            }
        }
        with pytest.raises(ValidationError) as exc_info:
            ClerkWebhook(**webhook_data)
        
        assert "type" in str(exc_info.value)


class TestGitHubModels:
    """Test GitHub integration models"""
    
    def test_github_permissions(self):
        """Test GitHubPermissions model"""
        perms = GitHubPermissions(admin=False, push=True, pull=True)
        assert perms.admin is False
        assert perms.push is True
        assert perms.pull is True
    
    def test_github_repository(self):
        """Test GitHubRepository model"""
        repo_data = {
            "id": 123456789,
            "name": "test-repo",
            "full_name": "user/test-repo",
            "private": False,
            "html_url": "https://github.com/user/test-repo",
            "description": "A test repository",
            "default_branch": "main",
            "permissions": {"admin": False, "push": True, "pull": True}
        }
        repo = GitHubRepository(**repo_data)
        assert repo.id == 123456789
        assert repo.name == "test-repo"
        assert repo.private is False
        assert repo.permissions.push is True
    
    def test_github_file(self):
        """Test GitHubFile model"""
        file_data = {
            "name": "auth.py",
            "path": "src/auth.py",
            "sha": "abc123def456",
            "size": 1024,
            "type": "file",
            "content": "IyBBdXRoIGNvZGU=",  # Base64 encoded
            "encoding": "base64"
        }
        file_obj = GitHubFile(**file_data)
        assert file_obj.name == "auth.py"
        assert file_obj.type == "file"
        assert file_obj.content == "IyBBdXRoIGNvZGU="
    
    def test_github_file_update(self):
        """Test GitHubFileUpdate model"""
        update_data = {
            "path": ".cogent/docs/src/auth.md",
            "content": "# Authentication Documentation\n\nThis module handles authentication.",
            "message": "📝 Update documentation for auth module",
            "branch": "main",
            "sha": "existing_sha_123"
        }
        update = GitHubFileUpdate(**update_data)
        assert update.path == ".cogent/docs/src/auth.md"
        assert "Authentication Documentation" in update.content
        assert update.message.startswith("📝")
        assert update.branch == "main"


class TestResponseModels:
    """Test API response models"""
    
    def test_projects_response(self):
        """Test ProjectsResponse model"""
        project_data = {
            "id": uuid4(),
            "name": "Test Project",
            "user_id": uuid4(),
            "github_repo_url": "https://github.com/test/repo",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "visibility": VisibilityEnum.PRIVATE,
            "branch_name": "main",
            "include_patterns": ["**/*"],
            "exclude_patterns": ["node_modules/**"]
        }
        project = Project(**project_data)
        
        response = ProjectsResponse(
            projects=[project],
            total=1,
            limit=20,
            offset=0
        )
        assert len(response.projects) == 1
        assert response.total == 1
        assert response.limit == 20
    
    def test_usage_stats_response(self):
        """Test UsageStatsResponse model"""
        response = UsageStatsResponse(
            total_operations=150,
            total_tokens=75000,
            total_cost=15.75,
            operations_by_type={"search": 100, "generate": 30, "mcp_call": 20},
            daily_usage=[
                {"date": "2024-01-15", "operations": 50, "tokens": 25000, "cost": 5.25},
                {"date": "2024-01-16", "operations": 100, "tokens": 50000, "cost": 10.50}
            ]
        )
        assert response.total_operations == 150
        assert response.operations_by_type["search"] == 100
        assert len(response.daily_usage) == 2


class TestErrorAndMCPModels:
    """Test error handling and MCP models"""
    
    def test_api_error(self):
        """Test ApiError model"""
        error = ApiError(
            error="validation_error",
            message="Invalid input provided",
            details={"field": "email", "issue": "Invalid email format"}
        )
        assert error.error == "validation_error"
        assert error.message == "Invalid input provided"
        assert error.details["field"] == "email"
    
    def test_document_context(self):
        """Test DocumentContext model"""
        context = DocumentContext(
            project_id=uuid4(),
            file_path="src/auth.py",
            content="def authenticate():\n    pass",
            summary="Authentication function",
            relevance_score=0.95
        )
        assert context.file_path == "src/auth.py"
        assert context.relevance_score == 0.95
    
    def test_context_request(self):
        """Test ContextRequest model"""
        request = ContextRequest(
            project_id=uuid4(),
            query="authentication functions",
            max_results=5
        )
        assert request.query == "authentication functions"
        assert request.max_results == 5
    
    def test_context_response(self):
        """Test ContextResponse model"""
        context = DocumentContext(
            project_id=uuid4(),
            file_path="src/auth.py",
            content="Authentication code",
            summary="Auth module"
        )
        
        response = ContextResponse(
            contexts=[context],
            total_found=1
        )
        assert len(response.contexts) == 1
        assert response.total_found == 1


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_get_language_from_path(self):
        """Test language detection from file paths"""
        assert get_language_from_path("src/auth.py") == "python"
        assert get_language_from_path("components/Button.tsx") == "typescript" 
        assert get_language_from_path("utils/helpers.js") == "javascript"
        assert get_language_from_path("models/User.java") == "java"
        assert get_language_from_path("services/api.go") == "go"
        assert get_language_from_path("main.rs") == "rust"
        assert get_language_from_path("config.yaml") == "yaml"
        assert get_language_from_path("README.md") == "markdown"
        assert get_language_from_path("unknown.xyz") is None  # Unknown extension
    
    def test_operation_type_enum(self):
        """Test OperationTypeEnum values"""
        assert OperationTypeEnum.SEARCH == "search"
        assert OperationTypeEnum.GENERATE == "generate"
        assert OperationTypeEnum.MCP_CALL == "mcp_call"
    
    def test_visibility_enum(self):
        """Test VisibilityEnum values"""
        assert VisibilityEnum.PRIVATE == "private"
        assert VisibilityEnum.PUBLIC == "public"
    
    def test_search_type_enum(self):
        """Test SearchTypeEnum values"""
        assert SearchTypeEnum.FULL_TEXT == "full_text"
        assert SearchTypeEnum.SEMANTIC == "semantic"
        assert SearchTypeEnum.HYBRID == "hybrid"