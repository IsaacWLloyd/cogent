# Sprint 0 Specification: Foundation & Contracts

## Overview
This document defines the complete technical specification for Sprint 0 - the foundation layer that all other teams will build upon. COGENT is a serverless application deployed on Vercel with Neon PostgreSQL database.

## Architecture Decisions

### 1. Database Schema - Extended Schema
```python
# Core entities with all required fields for MVP

User:
- id (UUID, primary key)
- clerk_id (string, unique, not null)
- email (string, unique, not null)
- name (string, not null)
- created_at (timestamp, not null)
- updated_at (timestamp, not null)
- settings_json (jsonb, nullable) # User preferences
- clerk_org_id (string, nullable) # For future team features
- last_seen (timestamp, nullable)

Project:
- id (UUID, primary key)
- name (string, not null)
- user_id (UUID, foreign key to User, not null)
- github_repo_url (string, not null)
- created_at (timestamp, not null)
- updated_at (timestamp, not null)
- description (text, nullable)
- visibility (enum: 'private'|'public', default='private')
- settings_json (jsonb, nullable) # Project-specific settings
- branch_name (string, default='main')
- include_patterns (text[], default=['**/*'])
- exclude_patterns (text[], default=['node_modules/**', '.git/**'])

Document:
- id (UUID, primary key)
- project_id (UUID, foreign key to Project, not null)
- file_path (string, not null) # Relative to repo root
- content (text, not null) # Generated documentation
- summary (text, not null) # Brief summary
- commit_hash (string, not null) # Git commit this doc corresponds to
- created_at (timestamp, not null)
- updated_at (timestamp, not null)
- version (integer, default=1) # Document version
- language (string, nullable) # Programming language detected
- imports (text[], nullable) # Detected imports/dependencies
- exports (text[], nullable) # Detected exports
- references (text[], nullable) # References to other files

SearchIndex:
- id (UUID, primary key)
- document_id (UUID, foreign key to Document, not null)
- content_vector (vector, nullable) # pgvector embedding
- full_text (tsvector, not null) # PostgreSQL full-text search
- relevance_scores (jsonb, nullable) # Cached relevance metrics
- metadata_json (jsonb, nullable) # Additional search metadata

Usage:
- id (UUID, primary key)
- project_id (UUID, foreign key to Project, not null)
- timestamp (timestamp, not null)
- operation_type (enum: 'search'|'generate'|'mcp_call', not null)
- tokens_used (integer, not null)
- cost (decimal, not null) # In USD
- llm_model (string, not null) # Model used for operation
- endpoint_called (string, not null) # API endpoint
- response_time (integer, nullable) # Response time in ms

ApiKey:
- id (UUID, primary key)
- project_id (UUID, foreign key to Project, not null)
- key_hash (string, not null) # SHA-256 hash of the API key
- name (string, not null) # User-friendly name
- created_at (timestamp, not null)
- last_used (timestamp, nullable)
```

### 2. API Structure - RESTful CRUD
```
# Clerk Webhooks
POST /api/webhooks/clerk

# Auth endpoints
GET  /api/v1/auth/session
POST /api/v1/auth/logout

# Core endpoints
GET    /api/v1/projects
POST   /api/v1/projects
GET    /api/v1/projects/{id}
PUT    /api/v1/projects/{id}
DELETE /api/v1/projects/{id}
GET    /api/v1/projects/{id}/documents
POST   /api/v1/projects/{id}/documents
POST   /api/v1/projects/{id}/search
GET    /api/v1/projects/{id}/api-keys
POST   /api/v1/projects/{id}/api-keys
DELETE /api/v1/projects/{id}/api-keys/{key_id}

# User endpoints
GET /api/v1/user/profile
PUT /api/v1/user/profile
GET /api/v1/user/usage

# GitHub integration
GET /api/v1/github/repos
GET /api/v1/github/repos/{owner}/{repo}/files
PUT /api/v1/github/repos/{owner}/{repo}/files
```

### 3. Clerk Integration - Basic Integration
- Webhook endpoint for user sync (create/update/delete)
- Middleware to validate Clerk session tokens
- Store clerk_id in User table
- Use Clerk's session for all authentication

### 4. MCP Server Communication - Direct Database Access
- MCP server connects directly to Neon database
- Shared SQLAlchemy models between backend and MCP server
- Connection pooling per serverless function
- No HTTP API calls needed for MCP operations

### 5. GitHub Integration - GitHub App
- Create official COGENT GitHub App
- OAuth flow for installation
- App-level permissions for repository access
- Webhook support ready for future features

### 6. Documentation Storage - Configurable with Structure Mirroring
- Default: `.cogent/docs/{original_path}.md`
- Mirrors entire project directory structure
- User-configurable via project settings
- Alternative: alongside source files
- Custom patterns supported

### 7. Mock Data - Realistic Test Data
- 3 test users with different Clerk IDs
- 5 test projects with varied settings
- 50+ documents with actual code examples
- Usage data for past 30 days
- Realistic search scenarios
- GitHub repository integration examples

## Implementation Plan

### Phase 1: Core Infrastructure
1. **Database Schema & Models**
   - SQLAlchemy models with Neon optimizations
   - Alembic migrations
   - Connection pooling configuration

2. **API Foundation**
   - FastAPI application structure
   - Vercel Function configuration
   - Request/response models
   - Error handling middleware

3. **Authentication Layer**
   - Clerk webhook handler
   - Session validation middleware
   - User sync logic

### Phase 2: Core Functionality
4. **Project Management**
   - CRUD operations for projects
   - GitHub repository validation
   - Settings management

5. **Document System**
   - Document storage and retrieval
   - Search index management
   - Content versioning

6. **GitHub Integration**
   - GitHub App setup
   - File read/write operations
   - Repository access validation

### Phase 3: Advanced Features
7. **Search & MCP**
   - Full-text search with PostgreSQL
   - Vector search with pgvector
   - MCP server implementation with PydanticAI

8. **Usage Tracking**
   - API usage monitoring
   - Billing integration preparation
   - Analytics dashboard data

### Phase 4: Testing & Documentation
9. **Mock Data Generation**
   - Realistic test data generators
   - Database seeding scripts
   - Development environment setup

10. **API Documentation**
    - Complete OpenAPI specification
    - Endpoint documentation
    - Integration examples

## Technical Constraints

### Vercel Serverless Limits
- Function timeout: 10s for API routes, 60s for MCP operations
- Memory limit: 1GB default, 3GB for MCP functions
- Cold start optimization required
- Stateless function design

### Neon Database
- Serverless PostgreSQL with connection pooling
- pgvector extension for embeddings
- Automatic scaling and connection management
- Optimized for serverless workloads

### Security Requirements
- All API keys hashed with SHA-256
- Clerk session token validation
- GitHub App permissions scoped minimally
- Environment variables for all secrets
- Rate limiting on all endpoints

## Success Criteria

### For Backend Team
- ✅ Complete database schema with migrations
- ✅ All API endpoints implemented and documented
- ✅ Clerk integration with user sync
- ✅ GitHub App integration working

### For Frontend Team
- ✅ Complete TypeScript types for all API responses
- ✅ Mock data available for development
- ✅ API client interfaces defined

### For MCP Team
- ✅ Database models available for direct access
- ✅ Search index structure defined
- ✅ PydanticAI integration patterns established

### For Search Team
- ✅ Document schema with search fields
- ✅ Search index structure ready
- ✅ Mock documents for testing

## File Structure
```
/
├── api/                    # FastAPI backend (single Vercel Function)
│   ├── main.py            # FastAPI app entry point
│   ├── models/            # SQLAlchemy models
│   ├── routers/           # API route handlers
│   ├── middleware/        # Auth and other middleware
│   └── services/          # Business logic
├── mcp/                   # PydanticAI MCP server (separate Function)
│   ├── main.py           # MCP server entry point
│   ├── agents/           # PydanticAI agents
│   └── tools/            # MCP tools
├── shared/               # Shared types and utilities
│   ├── types/            # TypeScript/Python type definitions
│   └── utils/            # Common utilities
├── frontend/             # React + Vite application
├── mock-data/            # Development data generators
├── vercel.json          # Vercel configuration
└── requirements.txt     # Python dependencies
```

This specification provides the complete foundation for Sprint 0 implementation.