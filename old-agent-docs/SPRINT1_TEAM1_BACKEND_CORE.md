# Sprint 1 Team 1: Backend Core Implementation

## Project Context

You are working on **COGENT** (Code Organization and Generation Enhancement Tool), a comprehensive documentation system that forces Claude Code to generate and maintain documentation for every code file it creates or modifies. 

**Sprint 0 has been completed** and established all foundational contracts:
- Complete OpenAPI specification (`openapi.yaml`)
- SQLAlchemy database models (`backend/models.py`) 
- Shared TypeScript and Python types (`shared/types.ts`, `shared/models.py`)
- Mock data generators (`backend/mock_data.py`)
- Monorepo structure with proper dependencies

## Your Team's Responsibilities

As the **Backend Core** team, you are responsible for implementing the FastAPI backend foundation that will serve as the core API for the entire COGENT system. Your deliverables include:

### Core Infrastructure
- FastAPI application structure with proper middleware, routing, and configuration
- SQLAlchemy database connection setup with support for both PostgreSQL (production) and SQLite (development)
- Basic CRUD endpoints for users, projects, and documents following the OpenAPI specification
- Mock authentication middleware (real OAuth implementation comes in Sprint 2)
- Comprehensive error handling patterns and HTTP status codes
- Structured logging infrastructure for debugging and monitoring

### API Endpoints to Implement

Based on the completed OpenAPI specification, you must implement these endpoints with mock authentication:

**Authentication (Mock Implementation)**
- `POST /auth/login` - Return mock JWT tokens
- `POST /auth/logout` - Clear auth state  
- `POST /auth/refresh` - Return new mock tokens

**Projects**
- `GET /projects` - List user's projects
- `POST /projects` - Create new project
- `GET /projects/{id}` - Get project details
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project

**Documents** 
- `GET /projects/{id}/documents` - List project documents
- `POST /projects/{id}/documents` - Create/update document

**Search**
- `POST /projects/{id}/search` - Search documents (basic implementation, advanced search comes in Sprint 1 Team 4)

**User Management**
- `GET /user/profile` - Get user profile
- `PUT /user/profile` - Update user profile  
- `GET /user/usage` - Get usage statistics

## Available Resources

You have access to these completed Sprint 0 deliverables:

1. **Database Schema** (`backend/models.py`): Complete SQLAlchemy models for User, Project, Document, and SearchIndex tables
2. **OpenAPI Specification** (`openapi.yaml`): Detailed API contracts with request/response schemas
3. **Shared Types** (`shared/types.ts`, `shared/models.py`): Type definitions for cross-component compatibility
4. **Mock Data** (`backend/mock_data.py`): Test data generators for realistic development
5. **Dependencies** (`backend/requirements.txt`): All required Python packages defined

## Technology Stack

- **Framework**: FastAPI with async/await support
- **Database**: SQLAlchemy ORM with PostgreSQL (production) / SQLite (development)
- **Authentication**: JWT tokens (mock implementation for now)
- **Validation**: Pydantic models (already defined in OpenAPI spec)
- **Logging**: Python logging with structured format
- **Testing**: Pytest for unit tests

## Knowledge Gaps & Questions

Before writing your detailed implementation specification, I need you to research the existing codebase and ask me specific questions about these areas where you need clarification:

### 1. Development Environment Setup
- What specific FastAPI configuration patterns should we follow?
- How should we structure the application factory pattern?
- What middleware stack do we need beyond the basics?
- How should we handle CORS for the frontend integration?

### 2. Database Configuration
- How should we handle database migrations? Should we use Alembic?
- What connection pooling strategy should we implement?
- How should we handle the PostgreSQL vs SQLite switching logic?
- What specific indexes do we need beyond what's in the models?

### 3. Error Handling Strategy
- What specific HTTP status codes should we return for each error type?
- How detailed should error messages be for security?
- Should we implement custom exception classes?
- What's our logging strategy for different environments (dev/prod)?

### 4. Mock Authentication Details
- What JWT payload structure should the mock implementation use?
- How should we validate the mock API keys for MCP server access?
- What user permissions model should we implement?
- How should we handle rate limiting in the mock implementation?

### 5. API Implementation Patterns
- Should we use FastAPI dependency injection for database sessions?
- What response format standards should we follow?
- How should we handle pagination for list endpoints?
- What caching strategy should we implement for read-heavy operations?

### 6. Integration Requirements
- How should the MCP server authenticate with our API?
- What's the exact format for the search endpoint responses?
- How should we handle file upload/update operations for documents?
- What background task patterns do we need for async operations?

## Your Task

1. **Research Phase**: Examine the existing Sprint 0 deliverables thoroughly
2. **Question Phase**: Ask me specific, focused questions about the knowledge gaps above, one area at a time
3. **Specification Phase**: Once all gaps are filled, write a comprehensive implementation specification that includes:
   - Detailed FastAPI application structure
   - Database setup and migration strategy
   - Complete endpoint implementations with error handling
   - Testing approach with specific test scenarios
   - Mock authentication implementation details
   - Integration points with other Sprint 1 teams

## Directory Restrictions

**CRITICAL: You are STRICTLY LIMITED to working within these directories:**
- `/backend/` - All FastAPI backend code
- `/shared/` - Only for reading shared types, NO modifications allowed
- Root level files: Only `requirements.txt` if needed for backend dependencies

**FORBIDDEN DIRECTORIES:**
- `/frontend/` - Assigned to Team 2
- `/mcp-server/` - Assigned to Team 3  
- `/hooks/` - Will be handled separately
- Any other directories not explicitly listed above

**File Creation Rules:**
- Create new files ONLY within `/backend/`
- Read existing files in `/shared/` for reference but DO NOT modify them
- If you need changes to shared types, ask for approval first

## Git Commit Guidelines

**Commit Strategy - Logical, Atomic Commits:**
1. **One Feature Per Commit** - Each commit should represent one complete, working feature
2. **Commit Early and Often** - Don't wait until everything is done
3. **Meaningful Messages** - Use conventional commit format

**Required Commit Pattern:**
```
feat(backend): add user authentication middleware
fix(backend): resolve database connection pooling issue  
docs(backend): add API endpoint documentation
test(backend): add unit tests for project CRUD operations
```

**Commit Frequency Guidelines:**
- After setting up basic FastAPI application structure
- After implementing each major endpoint group (auth, projects, documents, etc.)
- After adding error handling infrastructure
- After implementing logging setup
- After writing tests for each component
- Before integration with other teams

**Each commit must:**
- Pass all existing tests
- Include relevant test coverage for new code
- Have working, compilable code (no broken builds)
- Include clear commit message explaining the change

Remember: Your implementation must strictly adhere to the OpenAPI specification and database models from Sprint 0. Any deviations require explicit approval and updates to the contracts.

**Start by asking me your first set of questions about the development environment setup.**