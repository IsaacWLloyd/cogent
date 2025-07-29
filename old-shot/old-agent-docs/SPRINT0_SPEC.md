# PHASE0_SPEC.md - Sprint 0 Implementation Specification

## Overview
This document captures all architectural decisions for Sprint 0 of COGENT, serving as the definitive reference for implementation.

## Core Decisions

### 1. Database Schema - Minimal Schema
We will implement a minimal schema focusing on core functionality:

```sql
-- User table
User:
- id (UUID, primary key)
- email (string, unique, not null)
- name (string)
- github_id (string, unique, nullable)
- google_id (string, unique, nullable)
- created_at (timestamp)

-- Project table
Project:
- id (UUID, primary key)
- name (string, not null)
- user_id (UUID, foreign key to User)
- repo_url (string)
- api_key (string, unique, not null)
- created_at (timestamp)

-- Document table
Document:
- id (UUID, primary key)
- project_id (UUID, foreign key to Project)
- file_path (string, not null)
- content (text)
- summary (text)
- created_at (timestamp)
- updated_at (timestamp)

-- SearchIndex table
SearchIndex:
- id (UUID, primary key)
- document_id (UUID, foreign key to Document)
- content_vector (vector/array) -- For semantic search
- full_text (text) -- For full-text search
```

### 2. API Structure - RESTful CRUD
We will implement a standard RESTful API with the following endpoints:

```
Base URL: /api/v1

Authentication:
POST   /auth/login         - OAuth login (GitHub/Google)
POST   /auth/logout        - Clear auth cookies
POST   /auth/refresh       - Refresh access token

Projects:
GET    /projects           - List user's projects
POST   /projects           - Create new project
GET    /projects/{id}      - Get project details
PUT    /projects/{id}      - Update project
DELETE /projects/{id}      - Delete project

Documents:
GET    /projects/{id}/documents    - List project documents
POST   /projects/{id}/documents    - Create/update document

Search:
POST   /projects/{id}/search       - Search documents

User:
GET    /user/profile       - Get user profile
PUT    /user/profile       - Update user profile
GET    /user/usage         - Get usage statistics
```

### 3. Authentication - JWT with Refresh Tokens
- **Access Token**: 15 minute expiry, stored in httpOnly cookie
- **Refresh Token**: 7 day expiry, stored in httpOnly cookie
- **OAuth Flow**: GitHub and Google OAuth providers
- **API Keys**: No expiry, used by MCP server for project access

Token Structure:
```json
{
  "user_id": "uuid",
  "email": "user@example.com",
  "exp": 1234567890,
  "type": "access|refresh"
}
```

### 4. MCP Communication - HTTP API
The MCP server will communicate with the backend using simple HTTP requests:
- **Protocol**: HTTP POST requests to backend API
- **Authentication**: API key in Authorization header
- **Error Handling**: Exponential backoff retry logic
- **Timeout**: 30 second request timeout

Example flow:
```
MCP Server → POST /api/v1/projects/{id}/search
           ← 200 OK with relevant documents
```

### 5. Documentation Storage - Alongside Code Files
Documentation files will be stored in the same directory as the code:
- `src/auth.js` → `src/auth.md`
- `components/Button.tsx` → `components/Button.md`
- `services/api.py` → `services/api.md`

This approach:
- Keeps docs close to code
- Works with version control
- Easy to find related documentation
- Supports git branching naturally

### 6. Mock Data - Basic Dataset
Initial mock data will include:
- **1 test user** with OAuth connections
- **2-3 test projects** in different states
- **10-20 documents per project** with varied content
- **Simple search results** demonstrating relevance scoring

## Implementation Order

1. **Database Models** (SQLAlchemy)
2. **Shared Types** (TypeScript + Python)
3. **OpenAPI Specification**
4. **Mock Data Generators**
5. **Directory Structure Setup**

## Type Definitions

### Shared Types (TypeScript/Python)
```typescript
// User types
interface User {
  id: string;
  email: string;
  name?: string;
  githubId?: string;
  googleId?: string;
  createdAt: string;
}

// Project types
interface Project {
  id: string;
  name: string;
  userId: string;
  repoUrl?: string;
  apiKey: string;
  createdAt: string;
}

// Document types
interface Document {
  id: string;
  projectId: string;
  filePath: string;
  content: string;
  summary: string;
  createdAt: string;
  updatedAt: string;
}

// API types
interface LoginRequest {
  provider: 'github' | 'google';
  code: string;
}

interface SearchRequest {
  query: string;
  limit?: number;
  offset?: number;
}

interface SearchResult {
  documentId: string;
  filePath: string;
  content: string;
  relevanceScore: number;
}
```

## Additional Technical Decisions

### 7. Vector Database - PostgreSQL with pgvector
- **Extension**: pgvector for PostgreSQL
- **Dimensions**: 1536 (for text-embedding-ada-002 compatibility)
- **Fallback**: Full-text search using PostgreSQL GIN indexes
- **Development**: SQLite without vector support (full-text only)

### 8. LLM Provider - Gemini Flash via OpenRouter
- **Model**: google/gemini-flash-1.5 via OpenRouter
- **Configuration**: Environment variable `OPENROUTER_MODEL_URL` for flexibility
- **API Key**: `OPENROUTER_API_KEY` environment variable
- **Usage**: Document generation, search relevance validation

### 9. File Size Limits - No Restrictions
- **Decision**: No artificial limits on file sizes or project sizes
- **Rationale**: Let natural usage patterns emerge before optimization
- **Future**: Can add limits based on real usage data

## Implementation Status

✅ **COMPLETED**: All Sprint 0 deliverables
1. ✅ **OpenAPI Specification** - Complete API contract (`openapi.yaml`)
2. ✅ **Database Schema** - SQLAlchemy models with pgvector support (`backend/models.py`)
3. ✅ **Shared Types** - TypeScript and Python types (`shared/types.ts`, `shared/types.py`)
4. ✅ **Mock Data Generators** - Realistic test data (`backend/mock_data.py`)
5. ✅ **Monorepo Structure** - Complete project setup with dependencies

## File Structure Created

```
cogent/
├── package.json              # Root workspace configuration
├── .env.example              # Environment template
├── .gitignore               # Git ignore rules
├── openapi.yaml             # Complete API specification
├── PHASE0_SPEC.md           # This specification document
├── README.md                # Updated project documentation
├── backend/
│   ├── models.py            # SQLAlchemy database models
│   ├── mock_data.py         # Test data generation
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── package.json         # React + TypeScript setup
│   ├── vite.config.ts       # Vite configuration
│   └── README.md            # Frontend documentation
├── mcp-server/
│   ├── requirements.txt     # PydanticAI dependencies
│   └── README.md            # MCP server documentation
├── hooks/
│   ├── package.json         # Claude Code hooks setup
│   └── README.md            # Hooks documentation
└── shared/
    ├── types.ts             # TypeScript shared types
    ├── types.py             # Python shared types (Pydantic)
    ├── package.json         # Shared module setup
    └── tsconfig.json        # TypeScript configuration
```

## Ready for Parallel Development

All foundation contracts are complete. Teams can now work in parallel:
- **Backend Team**: Implement FastAPI endpoints using the OpenAPI spec
- **Frontend Team**: Build React components using shared TypeScript types
- **MCP Team**: Develop PydanticAI server using shared Python types
- **DevOps Team**: Set up deployment pipelines using the monorepo structure

All implementations must strictly follow these specifications to ensure compatibility.