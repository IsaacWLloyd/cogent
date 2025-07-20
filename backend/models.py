"""
SQLAlchemy models for COGENT database schema.
Supports both PostgreSQL (production) and SQLite (development).
"""

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, String, DateTime, ForeignKey, Text, Index, JSON, Integer, Float
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses CHAR(36) for SQLite.
    """
    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, str):
                return str(value)
            return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, str):
                return str(value)
            return value


def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = 'users'
    
    id = Column(GUID(), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    github_id = Column(String(255), unique=True, nullable=True, index=True)
    google_id = Column(String(255), unique=True, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(GUID(), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    user_id = Column(GUID(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    repo_url = Column(String(1024), nullable=True)
    api_key = Column(String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="projects")
    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_project_user', 'user_id'),
        Index('idx_project_api_key', 'api_key'),
    )
    
    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name})>"


class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(GUID(), primary_key=True, default=generate_uuid)
    project_id = Column(GUID(), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    file_path = Column(String(1024), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="documents")
    search_index = relationship("SearchIndex", back_populates="document", uselist=False, cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_document_project', 'project_id'),
        Index('idx_document_path', 'project_id', 'file_path'),
        Index('idx_document_updated', 'updated_at'),
    )
    
    def __repr__(self):
        return f"<Document(id={self.id}, file_path={self.file_path})>"


class SearchIndex(Base):
    __tablename__ = 'search_indexes'
    
    id = Column(GUID(), primary_key=True, default=generate_uuid)
    document_id = Column(GUID(), ForeignKey('documents.id', ondelete='CASCADE'), unique=True, nullable=False)
    
    # For PostgreSQL with pgvector extension
    content_vector = Column(Vector(1536), nullable=True)  # 1536 dimensions for text-embedding-ada-002
    
    # Full text search field
    full_text = Column(Text, nullable=False)
    
    # Relationships
    document = relationship("Document", back_populates="search_index")
    
    # Indexes
    __table_args__ = (
        Index('idx_search_document', 'document_id'),
        # PostgreSQL GIN index for full-text search
        Index('idx_search_fulltext', 'full_text', postgresql_using='gin'),
    )
    
    def __repr__(self):
        return f"<SearchIndex(id={self.id}, document_id={self.document_id})>"


# Optional: Usage tracking model for future implementation
class Usage(Base):
    __tablename__ = 'usage'
    
    id = Column(GUID(), primary_key=True, default=generate_uuid)
    project_id = Column(GUID(), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    tokens_used = Column(Integer, nullable=False, default=0)
    cost = Column(Float, nullable=False, default=0.0)
    operation_type = Column(String(50), nullable=False)  # 'document_generation', 'search', etc.
    operation_metadata = Column(JSON, nullable=True)  # Additional operation details
    
    # Relationships
    project = relationship("Project")
    
    # Indexes
    __table_args__ = (
        Index('idx_usage_project_time', 'project_id', 'timestamp'),
        Index('idx_usage_timestamp', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<Usage(id={self.id}, project_id={self.project_id}, tokens={self.tokens_used})>"