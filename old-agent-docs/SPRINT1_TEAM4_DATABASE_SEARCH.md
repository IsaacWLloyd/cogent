# Sprint 1 Team 4: Database & Search Implementation

## Project Context

You are working on **COGENT** (Code Organization and Generation Enhancement Tool), a comprehensive documentation system that forces Claude Code to generate and maintain documentation for every code file it creates or modifies.

**Sprint 0 has been completed** and established all foundational contracts:
- Complete SQLAlchemy database models (`backend/models.py`) with pgvector support
- OpenAPI specification (`openapi.yaml`) defining search endpoints
- Shared TypeScript and Python types (`shared/types.ts`, `shared/models.py`)
- Mock data generators (`backend/mock_data.py`) with realistic test data

## Your Team's Responsibilities

As the **Database & Search** team, you are responsible for implementing the core data storage and retrieval infrastructure that powers COGENT's intelligent documentation search. Your implementation will handle both traditional full-text search and semantic vector search capabilities.

### Core Infrastructure to Build

**Database Setup & Migrations**
- PostgreSQL setup with pgvector extension for production
- SQLite fallback configuration for development
- Alembic migration scripts for schema management
- Database connection pooling and session management
- Index optimization for search performance

**Search Implementation**
- Full-text search using PostgreSQL GIN indexes
- Vector embedding search using pgvector (1536 dimensions)
- Hybrid search combining full-text and semantic search
- Search result ranking and relevance scoring
- Query optimization and performance tuning

**Data Management**
- Database seeding scripts with realistic mock data
- Document indexing pipeline for search optimization
- Batch operations for large document sets
- Database backup and recovery procedures
- Performance monitoring and query analysis

**Integration Points**
- Search API endpoints that integrate with Backend Core team
- Document indexing that integrates with documentation pipeline
- Support for MCP Server search queries
- Analytics data collection for usage tracking

## Available Resources

You have access to these completed Sprint 0 deliverables:

1. **Database Models** (`backend/models.py`): Complete SQLAlchemy models with:
   - User, Project, Document, SearchIndex, and Usage tables
   - Proper foreign key relationships and cascading deletes
   - Optimized indexes for search operations
   - pgvector support for 1536-dimensional embeddings

2. **OpenAPI Specification** (`openapi.yaml`): Search endpoint contracts including:
   - `POST /projects/{id}/search` with SearchRequest/SearchResult schemas
   - Query parameters for filtering and pagination
   - Response formats for relevance scoring

3. **Mock Data** (`backend/mock_data.py`): Realistic test data generators for:
   - Multiple users with different project configurations
   - Diverse document types and content
   - Search scenarios with varying complexity

4. **Shared Models** (`shared/models.py`): Pydantic models for search requests and responses

## Technology Stack

- **Database**: PostgreSQL with pgvector extension (production) / SQLite (development)
- **ORM**: SQLAlchemy with async support
- **Migrations**: Alembic for schema management
- **Full-Text Search**: PostgreSQL GIN indexes with ts_vector
- **Vector Search**: pgvector with cosine similarity
- **Embeddings**: OpenRouter text-embedding-ada-002 (1536 dimensions)
- **Connection Pooling**: SQLAlchemy async engine with connection pooling
- **Testing**: Pytest with database fixtures

## Database Schema Overview

Your implementation will work with these models (already defined):

```python
# Document storage
class Document(Base):
    id: UUID
    project_id: UUID (FK)
    file_path: str
    content: text
    summary: text
    created_at: datetime
    updated_at: datetime

# Search optimization
class SearchIndex(Base):
    id: UUID
    document_id: UUID (FK, unique)
    content_vector: Vector(1536)  # pgvector for semantic search
    full_text: text               # Processed text for full-text search
```

## Knowledge Gaps & Questions

Before writing your detailed implementation specification, I need you to research the existing codebase and ask me specific questions about these areas where you need clarification:

### 1. Database Configuration Strategy
- How should we handle the PostgreSQL vs SQLite switching logic in different environments?
- What connection pooling configuration should we use for optimal performance?
- How should we structure database URL configuration and connection management?
- What's our strategy for handling database migrations in development vs production?

### 2. Search Algorithm Design
- How should we weight full-text search vs vector similarity in hybrid search?
- What preprocessing should we do on document content before indexing?
- How should we handle document chunking for large files?
- What relevance scoring algorithm should we implement for combining search types?

### 3. Vector Embedding Strategy
- When and how should we generate embeddings for new documents?
- Should we use batch processing or real-time embedding generation?
- How should we handle embedding API costs and rate limiting?
- What's our fallback strategy when vector search is unavailable?

### 4. Full-Text Search Implementation
- What text preprocessing should we apply (stemming, stop words, etc.)?
- How should we configure PostgreSQL ts_vector for optimal search results?
- What indexing strategy should we use for different document types?
- How should we handle search across multiple languages?

### 5. Performance Optimization
- What caching strategy should we implement for frequent search queries?
- How should we optimize database queries for large document collections?
- What indexing strategy will provide the best search performance?
- How should we handle search timeouts and query complexity limits?

### 6. Data Management & Seeding
- How should we structure the database seeding scripts for development?
- What realistic test data scenarios should we create?
- How should we handle data migration and schema updates?
- What backup and recovery procedures should we implement?

### 7. Integration Requirements
- How will the Backend Core team integrate with your search implementation?
- What API should you provide for document indexing operations?
- How should the MCP Server interact with your search functionality?
- What monitoring and analytics data should you collect?

### 8. Development & Testing
- How should we set up test databases for isolated testing?
- What fixtures should we create for search testing scenarios?
- How should we test both PostgreSQL and SQLite implementations?
- What performance benchmarks should we establish?

### 9. Deployment Considerations
- How should we handle database initialization in production?
- What environment variable configuration do we need?
- How should we manage database secrets and connection strings?
- What monitoring should we implement for database health?

### 10. Search Quality & Relevance
- How should we measure and improve search result quality?
- What metrics should we track for search performance?
- How should we handle edge cases (empty results, malformed queries)?
- What logging should we implement for search analytics?

## Your Task

1. **Research Phase**: Examine the existing Sprint 0 deliverables, especially the database models and mock data
2. **Question Phase**: Ask me specific, focused questions about the knowledge gaps above, one area at a time
3. **Specification Phase**: Once all gaps are filled, write a comprehensive implementation specification that includes:
   - Complete database setup and migration strategy
   - Detailed search implementation (full-text + vector)
   - Database seeding and test data management
   - Performance optimization and indexing strategy
   - Integration APIs for other teams
   - Testing approach with realistic search scenarios
   - Deployment and monitoring considerations

## Directory Restrictions

**CRITICAL: You are STRICTLY LIMITED to working within these directories:**
- `/backend/` - Database setup, migrations, and search implementation files
- `/shared/` - Only for reading shared types, NO modifications allowed
- Root level: Database configuration files (alembic.ini, etc.) if needed

**FORBIDDEN DIRECTORIES:**
- `/frontend/` - Assigned to Team 2
- `/mcp-server/` - Assigned to Team 3
- `/hooks/` - Will be handled separately
- Any other directories not explicitly listed above

**File Creation Rules:**
- Create database and search related files ONLY within `/backend/`
- Read existing files in `/shared/` for reference but DO NOT modify them
- If you need changes to shared types, ask for approval first
- Can create root-level database config files (alembic.ini, etc.) if needed for migrations

**Coordination with Team 1:**
- Team 1 (Backend Core) handles FastAPI app structure and endpoints
- You handle database setup, migrations, and search implementation
- Communicate any shared code needs through approved interfaces

## Git Commit Guidelines

**Commit Strategy - Logical, Atomic Commits:**
1. **One Feature Per Commit** - Each commit should represent one complete, working feature
2. **Commit Early and Often** - Don't wait until everything is done
3. **Meaningful Messages** - Use conventional commit format

**Required Commit Pattern:**
```
feat(db): setup PostgreSQL connection with pgvector extension
feat(db): add Alembic migrations for search schema
feat(db): implement full-text search with GIN indexes
feat(db): add vector embedding search functionality
test(db): add database seeding scripts with mock data
fix(db): optimize search query performance
```

**Commit Frequency Guidelines:**
- After setting up basic database connection and configuration
- After implementing Alembic migrations setup
- After creating database seeding scripts
- After implementing full-text search functionality
- After implementing vector search with pgvector
- After adding hybrid search combining both methods
- After implementing search result ranking and relevance scoring
- After adding performance optimizations and indexing
- After writing comprehensive tests

**Each commit must:**
- Pass all database tests and migrations
- Include relevant test coverage for search functionality
- Have working database setup (both PostgreSQL and SQLite)
- Include clear commit message explaining the change
- Follow database best practices and security guidelines

Remember: Your search implementation is the foundation that enables COGENT's intelligent documentation discovery. It must be fast, accurate, and scalable to handle growing document collections while providing relevant results to both human users and AI agents.

**Start by asking me your first set of questions about the database configuration strategy.**