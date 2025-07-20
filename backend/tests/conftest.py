"""
Test configuration and fixtures for COGENT backend tests.
"""

import pytest
import os
import tempfile
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Add parent directory to path for imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import create_app
from app.core.database import get_db
from models import Base, User, Project, Document, SearchIndex
from app.core.auth import jwt_manager


@pytest.fixture(scope="session")
def test_db():
    """Create test database"""
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp()
    database_url = f"sqlite:///{db_path}"
    
    # Set test database URL
    os.environ["DATABASE_URL"] = database_url
    
    # Create engine and tables
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def db_session(test_db):
    """Create database session for tests"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """Create test client with database dependency override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_user(db_session):
    """Create test user"""
    from datetime import datetime
    user = User(
        id=str(uuid.uuid4()),
        email="test@example.com",
        name="Test User",
        github_id="123456",
        created_at=datetime.utcnow()
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_project(db_session, test_user):
    """Create test project"""
    from datetime import datetime
    project = Project(
        id=str(uuid.uuid4()),
        name="Test Project",
        user_id=test_user.id,
        repo_url="https://github.com/test/repo",
        api_key=str(uuid.uuid4()),
        created_at=datetime.utcnow()
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)
    return project


@pytest.fixture
def test_document(db_session, test_project):
    """Create test document"""
    from datetime import datetime
    document = Document(
        id=str(uuid.uuid4()),
        project_id=test_project.id,
        file_path="src/test.py",
        content="# Test file\nprint('hello world')",
        summary="Test Python file",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)
    
    # Create search index
    search_index = SearchIndex(
        id=str(uuid.uuid4()),
        document_id=document.id,
        full_text=document.content
    )
    db_session.add(search_index)
    db_session.commit()
    
    return document


@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers with valid JWT token"""
    access_token = jwt_manager.create_access_token(
        user_id=str(test_user.id),
        email=test_user.email
    )
    return {"Cookie": f"access_token={access_token}"}