# Sprint 0: Foundation & Contracts - Implementation Guide

## Context
You are implementing Sprint 0 of the COGENT project, which is the critical foundation that all other teams will build upon. This sprint must be completed before any parallel work can begin.

## Available Information

### Project Overview
COGENT is a tool that forces Claude Code to generate and maintain comprehensive documentation for every code file it creates or modifies. Key components:
- FastAPI backend with PostgreSQL/SQLite
- React frontend with SHADCN UI
- PydanticAI MCP server for documentation search
- Claude Code hooks for documentation generation

### Your Deliverables
1. **OpenAPI Specification** - Complete API contract for all endpoints
2. **Database Schema** - SQLAlchemy models for all entities
3. **Shared Types** - TypeScript/Python types used across components
4. **Mock Data Generators** - Realistic test data for all entities
5. **Monorepo Structure** - Proper project setup with dependencies

## Knowledge Gaps & Questions

I need to gather specific requirements before implementing Sprint 0. ask me these questions one at a time, use my answers to construct a PHASE0_SPEC.md.

### Question 1: Database Schema Design

For the core entities, which schema structure should we use?

**A) Minimal Schema (Recommended)**
```python
- User (id, email, name, github_id, google_id, created_at)
- Project (id, name, user_id, repo_url, api_key, created_at)
- Document (id, project_id, file_path, content, summary, created_at, updated_at)
- SearchIndex (id, document_id, content_vector, full_text)
```

**B) Extended Schema**
```python
- User (+ avatar_url, settings_json, last_login)
- Project (+ description, visibility, settings_json, usage_quota)
- Document (+ version, language, imports, exports, references)
- SearchIndex (+ relevance_scores, metadata)
- Usage (id, project_id, timestamp, tokens_used, cost)
- TeamMember (id, project_id, user_id, role)
```

**C) Full Feature Schema**
```python
All of B plus:
- DocumentVersion (track all changes)
- Template (custom documentation templates)
- Integration (third-party connections)
- Webhook (external notifications)
- AuditLog (all actions tracked)
```

Please select: **[A]**, [B], or [C]

---

### Question 2: API Endpoint Structure

Which API structure should we implement?

**A) RESTful CRUD (Recommended)**
```
/api/v1/auth/login
/api/v1/auth/logout
/api/v1/projects (GET, POST)
/api/v1/projects/{id} (GET, PUT, DELETE)
/api/v1/projects/{id}/documents (GET, POST)
/api/v1/projects/{id}/search (POST)
/api/v1/user/profile (GET, PUT)
/api/v1/user/usage (GET)
```

**B) Action-Based**
```
/api/v1/auth/login
/api/v1/projects/create
/api/v1/projects/list
/api/v1/documents/generate
/api/v1/documents/search
/api/v1/context/retrieve
```

**C) GraphQL**
```
Single endpoint with queries and mutations
More flexible but more complex
```

Please select: **[A]**, [B], or [C]

---

### Question 3: Authentication Flow

Which authentication implementation should we use?

**A) JWT with Refresh Tokens (Recommended)**
```python
- Access token (15 min expiry)
- Refresh token (7 days)
- OAuth flow stores tokens in httpOnly cookies
- API keys for MCP server (no expiry)
```

**B) Simple JWT**
```python
- Single JWT token (24 hour expiry)
- Token in Authorization header
- API keys for MCP server
```

**C) Session-Based**
```python
- Server-side sessions with Redis
- Session cookies
- More secure but requires Redis
```

Please select: **[A]**, [B], or [C]

---

### Question 4: MCP Communication Protocol

How should the MCP server communicate with the backend?

**A) HTTP API with Polling (Recommended)**
```python
- MCP → Backend: HTTP POST requests
- Polling for updates every 5 seconds
- Simple retry logic
- Works everywhere
```

**B) WebSocket**
```python
- Persistent connection
- Real-time updates
- More complex error handling
- Better performance
```

**C) Message Queue**
```python
- Redis/RabbitMQ queue
- Async processing
- Most scalable
- Requires additional infrastructure
```

Please select: **[A]**, [B], or [C]

---

### Question 5: File Structure for Documentation

Where should documentation files be stored?

**A) Alongside Code Files (Recommended)**
```
src/auth.js → src/auth.md
components/Button.tsx → components/Button.md
services/api.py → services/api.md
```

**B) Separate Docs Directory**
```
src/auth.js → .cogent/docs/src/auth.md
Centralized documentation folder
```

**C) Database Only**
```
No file generation, only database storage
Accessed via API
```

Please select: **[A]**, [B], or [C]

---

### Question 6: Mock Data Complexity

What level of mock data should we generate?

**A) Basic Mock Data (Recommended)**
```python
- 1 test user
- 2-3 test projects
- 10-20 documents per project
- Simple search results
```

**B) Realistic Mock Data**
```python
- 5 users with different roles
- 10 projects with various states
- 100+ documents with real code examples
- Realistic search scenarios
```

**C) Minimal Mock Data**
```python
- Just enough to test endpoints
- Single examples only
```

Please select: **[A]**, [B], or [C]

---

## Implementation Instructions

Once we've answered these questions, you will proceed to:

1. Create the complete OpenAPI specification
2. Generate SQLAlchemy models
3. Create shared TypeScript/Python types
4. Build mock data generators
5. Set up the monorepo structure

ASK THEM ONE AT A TIME IN ORDER> ASK ANYTHING MORE YOU MIGHT THINK NECESSARY.

