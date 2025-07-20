"""
Database initialization script for COGENT backend.
Creates tables and populates with mock data for development.
"""

import asyncio
import logging
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import create_database_engine, SessionLocal
from app.core.config import get_settings
from app.core.logging_config import setup_logging
from models import Base, User, Project, Document, SearchIndex
from mock_data import generate_complete_dataset
from shared.models import User as UserSchema

logger = logging.getLogger(__name__)


def init_database():
    """Initialize database with tables and mock data"""
    # Setup logging
    setup_logging()
    logger.info("Starting database initialization")
    
    # Get settings
    settings = get_settings()
    logger.info(f"Database URL: {settings.database_url}")
    
    # Create engine and tables
    engine = create_database_engine()
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if we already have data
        existing_users = db.query(User).count()
        if existing_users > 0:
            logger.info(f"Database already has {existing_users} users, skipping mock data")
            return
        
        # Generate mock data
        logger.info("Generating mock data...")
        dataset = generate_complete_dataset()
        
        # Insert users
        for user_data in dataset["users"]:
            user = User(
                id=user_data["id"],
                email=user_data["email"],
                name=user_data["name"],
                github_id=user_data["github_id"],
                google_id=user_data["google_id"],
                created_at=user_data["created_at"]
            )
            db.add(user)
        
        # Insert projects
        for project_data in dataset["projects"]:
            project = Project(
                id=project_data["id"],
                name=project_data["name"],
                user_id=project_data["user_id"],
                repo_url=project_data["repo_url"],
                api_key=project_data["api_key"],
                created_at=project_data["created_at"]
            )
            db.add(project)
        
        # Insert documents
        for doc_data in dataset["documents"]:
            document = Document(
                id=doc_data["id"],
                project_id=doc_data["project_id"],
                file_path=doc_data["file_path"],
                content=doc_data["content"],
                summary=doc_data["summary"],
                created_at=doc_data["created_at"],
                updated_at=doc_data["updated_at"]
            )
            db.add(document)
        
        # Insert search indexes
        for search_data in dataset["search_indexes"]:
            search_index = SearchIndex(
                id=search_data["id"],
                document_id=search_data["document_id"],
                full_text=search_data["full_text"],
                content_vector=None  # Leave null for now
            )
            db.add(search_index)
        
        # Commit all changes
        db.commit()
        
        logger.info("Mock data inserted successfully")
        logger.info(f"Created {len(dataset['users'])} users")
        logger.info(f"Created {len(dataset['projects'])} projects")
        logger.info(f"Created {len(dataset['documents'])} documents")
        logger.info(f"Created {len(dataset['search_indexes'])} search indexes")
        
        # Update auth.py mock users with actual data
        test_user = dataset["users"][0]
        logger.info(f"Test user for authentication: {test_user['email']} (ID: {test_user['id']})")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()
    
    logger.info("Database initialization completed")


if __name__ == "__main__":
    init_database()