"""
SQLAlchemy models optimized for Neon PostgreSQL
These models implement the Extended Schema from SPRINT0_SPEC.md
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import uuid4
import enum

from sqlalchemy import (
    Column, String, DateTime, Text, Integer, Numeric, Boolean,
    ForeignKey, JSON, ARRAY, Enum as SQLEnum, UniqueConstraint,
    Index, CheckConstraint
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class VisibilityEnum(enum.Enum):
    """Project visibility options"""
    PRIVATE = "private"
    PUBLIC = "public"


class OperationTypeEnum(enum.Enum):
    """Usage operation types"""
    SEARCH = "search"
    GENERATE = "generate"
    MCP_CALL = "mcp_call"


class User(Base):
    """User entity with Clerk integration"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    clerk_id = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    
    # Extended fields
    settings_json = Column(JSON, nullable=True)
    clerk_org_id = Column(String(255), nullable=True, index=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Project(Base):
    """Project entity with GitHub integration"""
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    github_repo_url = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    
    # Extended fields
    description = Column(Text, nullable=True)
    visibility = Column(SQLEnum(VisibilityEnum), nullable=False, default=VisibilityEnum.PRIVATE)
    settings_json = Column(JSON, nullable=True)
    branch_name = Column(String(255), nullable=False, default="main")
    include_patterns = Column(ARRAY(String), nullable=False, default=["**/*"])
    exclude_patterns = Column(ARRAY(String), nullable=False, default=["node_modules/**", ".git/**"])
    
    # Relationships
    user = relationship("User", back_populates="projects")
    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")
    api_keys = relationship("ApiKey", back_populates="project", cascade="all, delete-orphan")
    usage_records = relationship("Usage", back_populates="project", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'github_repo_url', name='unique_user_repo'),
        Index('idx_project_user_created', 'user_id', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, repo={self.github_repo_url})>"


class Document(Base):
    """Document entity with version tracking"""
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    file_path = Column(String(1000), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    commit_hash = Column(String(40), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    
    # Extended fields
    version = Column(Integer, nullable=False, default=1)
    language = Column(String(50), nullable=True, index=True)
    imports = Column(ARRAY(String), nullable=True)
    exports = Column(ARRAY(String), nullable=True)
    references = Column(ARRAY(String), nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="documents")
    search_index = relationship("SearchIndex", back_populates="document", cascade="all, delete-orphan", uselist=False)
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('project_id', 'file_path', 'commit_hash', name='unique_project_file_commit'),
        Index('idx_document_project_path', 'project_id', 'file_path'),
        Index('idx_document_language', 'language'),
        Index('idx_document_commit', 'commit_hash'),
    )
    
    def __repr__(self):
        return f"<Document(id={self.id}, path={self.file_path}, commit={self.commit_hash[:8]})>"


class SearchIndex(Base):
    """Search index for documents with full-text and vector search"""
    __tablename__ = "search_indexes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False, unique=True, index=True)
    content_vector = Column(Vector(1536), nullable=True)  # OpenAI ada-002 embedding size
    full_text = Column(TSVECTOR, nullable=False)
    
    # Extended fields
    relevance_scores = Column(JSON, nullable=True)
    metadata_json = Column(JSON, nullable=True)
    
    # Relationships
    document = relationship("Document", back_populates="search_index")
    
    # Indexes for search optimization
    __table_args__ = (
        Index('idx_search_fulltext', 'full_text', postgresql_using='gin'),
        Index('idx_search_vector', 'content_vector', postgresql_using='ivfflat', postgresql_with={'lists': 100}),
    )
    
    def __repr__(self):
        return f"<SearchIndex(id={self.id}, document_id={self.document_id})>"


class Usage(Base):
    """Usage tracking for billing and analytics"""
    __tablename__ = "usage"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=func.now(), index=True)
    operation_type = Column(SQLEnum(OperationTypeEnum), nullable=False, index=True)
    tokens_used = Column(Integer, nullable=False)
    cost = Column(Numeric(10, 6), nullable=False)  # 6 decimal places for precise cost tracking
    
    # Extended fields
    llm_model = Column(String(100), nullable=False, index=True)
    endpoint_called = Column(String(200), nullable=False)
    response_time = Column(Integer, nullable=True)  # Response time in milliseconds
    
    # Relationships
    project = relationship("Project", back_populates="usage_records")
    
    # Constraints and indexes
    __table_args__ = (
        CheckConstraint('tokens_used >= 0', name='positive_tokens'),
        CheckConstraint('cost >= 0', name='positive_cost'),
        Index('idx_usage_project_timestamp', 'project_id', 'timestamp'),
        Index('idx_usage_operation_type', 'operation_type'),
        Index('idx_usage_model', 'llm_model'),
    )
    
    def __repr__(self):
        return f"<Usage(id={self.id}, project_id={self.project_id}, type={self.operation_type}, cost=${self.cost})>"


class ApiKey(Base):
    """API keys for MCP server access"""
    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    key_hash = Column(String(64), nullable=False, unique=True, index=True)  # SHA-256 hash
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    last_used = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="api_keys")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('project_id', 'name', name='unique_project_key_name'),
        Index('idx_apikey_project', 'project_id'),
        Index('idx_apikey_hash', 'key_hash'),
    )
    
    def __repr__(self):
        return f"<ApiKey(id={self.id}, name={self.name}, project_id={self.project_id})>"


# Database configuration for Neon
class DatabaseConfig:
    """Database configuration optimized for Neon serverless PostgreSQL"""
    
    # Connection settings optimized for serverless
    POOL_SIZE = 0  # No persistent connections in serverless
    MAX_OVERFLOW = 10  # Allow temporary connections
    POOL_TIMEOUT = 30  # Connection timeout in seconds
    POOL_RECYCLE = 1800  # Recycle connections after 30 minutes
    POOL_PRE_PING = True  # Verify connections before use
    
    # Neon-specific optimizations
    CONNECT_ARGS = {
        "application_name": "cogent",
        "connect_timeout": 10,
        "command_timeout": 60,
        "server_settings": {
            "jit": "off",  # Disable JIT for faster cold starts
            "shared_preload_libraries": "pg_stat_statements,pgvector",
        }
    }


# Utility functions for common queries
class DatabaseQueries:
    """Common database query patterns optimized for Neon"""
    
    @staticmethod
    def get_user_by_clerk_id(session: Session, clerk_id: str) -> Optional[User]:
        """Get user by Clerk ID with optimized query"""
        return session.query(User).filter(User.clerk_id == clerk_id).first()
    
    @staticmethod
    def get_project_documents(session: Session, project_id: str, limit: int = 50, offset: int = 0) -> List[Document]:
        """Get project documents with pagination"""
        return (
            session.query(Document)
            .filter(Document.project_id == project_id)
            .order_by(Document.updated_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
    
    @staticmethod
    def search_documents_fulltext(session: Session, project_id: str, query: str, limit: int = 10) -> List[tuple]:
        """Full-text search with ranking"""
        return (
            session.query(Document, SearchIndex)
            .join(SearchIndex)
            .filter(Document.project_id == project_id)
            .filter(SearchIndex.full_text.match(query))
            .order_by(func.ts_rank(SearchIndex.full_text, func.plainto_tsquery(query)).desc())
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_usage_stats(session: Session, project_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get usage statistics for date range"""
        result = (
            session.query(
                func.count(Usage.id).label('total_operations'),
                func.sum(Usage.tokens_used).label('total_tokens'),
                func.sum(Usage.cost).label('total_cost'),
                Usage.operation_type
            )
            .filter(Usage.project_id == project_id)
            .filter(Usage.timestamp >= start_date)
            .filter(Usage.timestamp <= end_date)
            .group_by(Usage.operation_type)
            .all()
        )
        
        stats = {
            'total_operations': 0,
            'total_tokens': 0,
            'total_cost': 0,
            'operations_by_type': {}
        }
        
        for row in result:
            stats['total_operations'] += row.total_operations
            stats['total_tokens'] += row.total_tokens or 0
            stats['total_cost'] += float(row.total_cost or 0)
            stats['operations_by_type'][row.operation_type.value] = row.total_operations
            
        return stats


# Export all models for easy import
__all__ = [
    'Base',
    'User',
    'Project', 
    'Document',
    'SearchIndex',
    'Usage',
    'ApiKey',
    'VisibilityEnum',
    'OperationTypeEnum',
    'DatabaseConfig',
    'DatabaseQueries'
]