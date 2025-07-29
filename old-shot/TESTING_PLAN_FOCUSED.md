# Focused Testing Plan: API Models & Migrations

## Overview
Essential testing for SQLAlchemy models, Pydantic validation, and database migrations to ensure solid foundation.

## Test Structure (Simplified)
```
tests/
├── test_models.py         # SQLAlchemy model tests
├── test_pydantic.py       # Pydantic model validation
├── test_migrations.py     # Database migration tests
├── conftest.py           # Pytest configuration
└── factories.py          # Test data factories
```

## What We'll Test

### 1. SQLAlchemy Models (`test_models.py`)
```python
# Test each model's core functionality
- User model: relationships, constraints, Clerk integration
- Project model: GitHub URL validation, pattern arrays
- Document model: file path uniqueness, version handling
- ApiKey model: hash generation, project relationships
- Usage model: cost calculations, timestamp handling
- SearchIndex model: vector operations, full-text search
```

### 2. Pydantic Validation (`test_pydantic.py`)
```python
# Test API request/response models
- CreateProjectRequest: required fields, URL validation
- SearchRequest: query validation, filter handling
- ClerkWebhook: event type validation, data structure
- GitHubFile: content encoding, type validation
- All response models: serialization consistency
```

### 3. Database Migrations (`test_migrations.py`)
```python
# Test database schema changes
- Migration up/down operations
- Index creation (especially for search)
- Constraint enforcement
- Data integrity during migrations
```

## Implementation Plan (3-4 hours)

### Phase 1: Setup (30 minutes)
```bash
# Add test dependencies to requirements.txt
pytest==7.4.3
pytest-asyncio==0.21.1
factory-boy==3.3.0
sqlalchemy-utils==0.41.1
pytest-cov==4.1.0

# Create test database configuration
```

### Phase 2: Model Tests (2 hours)
```python
# Example: test_models.py structure
def test_user_model_creation():
    """Test User model basic creation and validation"""

def test_user_clerk_id_uniqueness():
    """Test Clerk ID uniqueness constraint"""

def test_project_github_url_validation():
    """Test GitHub URL format validation"""

def test_document_file_path_uniqueness():
    """Test unique constraint on project_id + file_path + commit_hash"""

def test_api_key_hash_generation():
    """Test API key hash creation and validation"""

def test_usage_cost_calculation():
    """Test usage cost calculation accuracy"""

def test_search_index_relationships():
    """Test SearchIndex to Document relationship"""
```

### Phase 3: Pydantic Tests (1 hour)
```python
# Example: test_pydantic.py structure
def test_create_project_request_validation():
    """Test project creation request validation"""

def test_search_request_filters():
    """Test search request filter validation"""

def test_clerk_webhook_parsing():
    """Test Clerk webhook data parsing"""

def test_response_serialization():
    """Test API response model serialization"""
```

### Phase 4: Migration Tests (30 minutes)
```python
# Example: test_migrations.py structure
def test_migration_up_down():
    """Test migration reversibility"""

def test_indexes_created():
    """Test that all indexes are properly created"""

def test_constraints_enforced():
    """Test database constraints work correctly"""
```

## Test Configuration

### conftest.py
```python
import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared.database import Base

@pytest.fixture
def test_db():
    """Create test database"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def sample_user(test_db):
    """Create test user"""
    from shared.database import User
    user = User(
        clerk_id="test_clerk_123",
        email="test@example.com",
        name="Test User"
    )
    test_db.add(user)
    test_db.commit()
    return user
```

### factories.py
```python
import factory
from shared.database import User, Project, Document

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    clerk_id = factory.Sequence(lambda n: f"clerk_{n}")
    email = factory.Faker('email')
    name = factory.Faker('name')

class ProjectFactory(factory.Factory):
    class Meta:
        model = Project
    
    name = factory.Faker('company')
    github_repo_url = factory.Faker('url')
    user = factory.SubFactory(UserFactory)
```

## Key Test Cases

### Critical Model Validation
1. **Unique Constraints**: Ensure database constraints work
2. **Required Fields**: Test all non-nullable fields
3. **Relationships**: Test foreign key relationships
4. **Data Types**: Test field type validation
5. **Indexes**: Ensure search indexes function

### Critical Pydantic Validation
1. **Request Models**: All API input validation
2. **Response Models**: Serialization consistency
3. **Type Conversion**: Automatic type handling
4. **Error Messages**: Clear validation errors

### Critical Migration Tests
1. **Schema Creation**: All tables and indexes
2. **Constraint Enforcement**: Foreign keys, unique constraints
3. **Data Migration**: Any data transformation logic

## Simple Test Examples

### Model Test
```python
def test_project_model(test_db, sample_user):
    """Test Project model creation and relationships"""
    project = Project(
        name="Test Project",
        github_repo_url="https://github.com/user/repo",
        user_id=sample_user.id
    )
    test_db.add(project)
    test_db.commit()
    
    assert project.id is not None
    assert project.user.id == sample_user.id
    assert project.visibility == VisibilityEnum.PRIVATE  # default
```

### Pydantic Test
```python
def test_create_project_request():
    """Test CreateProjectRequest validation"""
    from shared.models import CreateProjectRequest
    
    # Valid request
    valid_data = {
        "name": "My Project",
        "github_repo_url": "https://github.com/user/repo"
    }
    request = CreateProjectRequest(**valid_data)
    assert request.name == "My Project"
    
    # Invalid URL
    with pytest.raises(ValidationError):
        CreateProjectRequest(name="Project", github_repo_url="invalid-url")
```

## Success Criteria
- ✅ All models can be created/saved/retrieved
- ✅ All constraints are enforced
- ✅ All Pydantic models validate correctly
- ✅ Migrations run successfully up and down
- ✅ 90%+ coverage on model/validation code

## Timeline: 3-4 hours total
1. **Setup** (30 min): Test infrastructure
2. **Models** (2 hours): SQLAlchemy model tests
3. **Pydantic** (1 hour): Request/response validation
4. **Migrations** (30 min): Database migration tests

This focused approach ensures the foundation is solid without over-engineering. Should I proceed with implementing these essential tests?