"""
Simple database initialization script without FastAPI dependencies.
"""

import os
import sys
import uuid
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Base, User, Project, Document, SearchIndex


def init_simple_database():
    """Initialize database with basic tables and one test user"""
    
    # Create SQLite database
    database_url = "sqlite:///./cogent.db"
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if we already have data
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"Database already has {existing_users} users, skipping initialization")
            return
        
        # Create test user
        user_id = str(uuid.uuid4())
        user = User(
            id=user_id,
            email="test@example.com",
            name="Test User",
            github_id="123456",
            google_id=None,
            created_at=datetime.utcnow()
        )
        db.add(user)
        
        # Create test project
        project_id = str(uuid.uuid4())
        project = Project(
            id=project_id,
            name="Test Project",
            user_id=user_id,
            repo_url="https://github.com/test/repo",
            api_key=str(uuid.uuid4()),
            created_at=datetime.utcnow()
        )
        db.add(project)
        
        # Create test document
        doc_id = str(uuid.uuid4())
        document = Document(
            id=doc_id,
            project_id=project_id,
            file_path="src/hello.py",
            content="# Hello World\nprint('Hello, COGENT!')\n\ndef greet(name):\n    return f'Hello, {name}!'",
            summary="Simple Python hello world script with greeting function",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(document)
        
        # Create search index
        search_index = SearchIndex(
            id=str(uuid.uuid4()),
            document_id=doc_id,
            full_text=document.content,
            content_vector=None
        )
        db.add(search_index)
        
        # Commit changes
        db.commit()
        
        print("Database initialized successfully!")
        print(f"Test user: {user.email} (ID: {user_id})")
        print(f"Test project: {project.name} (ID: {project_id})")
        print(f"Test document: {document.file_path} (ID: {doc_id})")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_simple_database()