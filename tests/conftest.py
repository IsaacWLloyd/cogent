"""
Test configuration and fixtures for COGENT testing
"""

import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import tempfile
import os
from datetime import datetime
from uuid import uuid4

# Add shared module to path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from shared.database import Base, User, Project, Document, ApiKey, Usage, VisibilityEnum, OperationTypeEnum


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_db() -> Session:
    """Create test database with SQLite in-memory"""
    # Use SQLite for fast testing
    engine = create_engine(
        "sqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={
            "check_same_thread": False,
        },
        echo=False  # Set to True for SQL debugging
    )
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def sample_user(test_db: Session) -> User:
    """Create a sample user for testing"""
    user = User(
        id=uuid4(),
        clerk_id=f"user_clerk_{uuid4().hex[:12]}",
        email="test@example.com",
        name="Test User",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        settings_json={"theme": "light"}
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def sample_project(test_db: Session, sample_user: User) -> Project:
    """Create a sample project for testing"""
    project = Project(
        id=uuid4(),
        name="Test Project",
        user_id=sample_user.id,
        github_repo_url="https://github.com/test/repo",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        description="Test project description",
        visibility=VisibilityEnum.PRIVATE,
        branch_name="main",
        include_patterns=["**/*"],
        exclude_patterns=["node_modules/**", ".git/**"]
    )
    test_db.add(project)
    test_db.commit()
    test_db.refresh(project)
    return project


@pytest.fixture
def sample_document(test_db: Session, sample_project: Project) -> Document:
    """Create a sample document for testing"""
    document = Document(
        id=uuid4(),
        project_id=sample_project.id,
        file_path="src/auth.py",
        content="# Authentication module\ndef login():\n    pass",
        summary="Authentication module with login function",
        commit_hash="abc123def456",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        version=1,
        language="python",
        imports=["hashlib", "jwt"],
        exports=["login", "logout"],
        references=["src/utils.py"]
    )
    test_db.add(document)
    test_db.commit()
    test_db.refresh(document)
    return document


@pytest.fixture
def sample_api_key(test_db: Session, sample_project: Project) -> ApiKey:
    """Create a sample API key for testing"""
    api_key = ApiKey(
        id=uuid4(),
        project_id=sample_project.id,
        key_hash="hashed_api_key_12345",
        name="Test API Key",
        created_at=datetime.now(),
        last_used=datetime.now()
    )
    test_db.add(api_key)
    test_db.commit()
    test_db.refresh(api_key)
    return api_key


@pytest.fixture
def sample_usage(test_db: Session, sample_project: Project) -> Usage:
    """Create a sample usage record for testing"""
    usage = Usage(
        id=uuid4(),
        project_id=sample_project.id,
        timestamp=datetime.now(),
        operation_type=OperationTypeEnum.SEARCH,
        tokens_used=1500,
        cost=0.15,
        llm_model="openai/gpt-4-turbo",
        endpoint_called="/api/v1/search",
        response_time=250
    )
    test_db.add(usage)
    test_db.commit()
    test_db.refresh(usage)
    return usage


# Helper functions for tests
def assert_datetime_close(dt1: datetime, dt2: datetime, tolerance_seconds: int = 5):
    """Assert two datetimes are close within tolerance"""
    diff = abs((dt1 - dt2).total_seconds())
    assert diff <= tolerance_seconds, f"Datetimes differ by {diff} seconds"