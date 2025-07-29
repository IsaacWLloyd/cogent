# Sprint 0: Foundation & Contracts - Implementation Guide (Serverless Architecture)

## Context
You are implementing Sprint 0 of the COGENT project, which is the critical foundation that all other teams will build upon. This sprint must be completed before any parallel work can begin.

## Architecture Overview
COGENT is a Claude Code enhancement tool deployed as a serverless application on Vercel:
- **Backend**: FastAPI as single Vercel Function (`/api/*`)
- **Frontend**: React + Vite + SHADCN UI (static deployment)
- **MCP Server**: PydanticAI as separate Vercel Function (`/mcp/*`)
- **Database**: Neon (serverless PostgreSQL with pgvector)
- **Auth**: Clerk for user authentication and management
- **Storage**: Documentation stored in user's GitHub repositories

## Your Deliverables
1. **OpenAPI Specification** - Complete API contract for all endpoints
2. **Database Schema** - SQLAlchemy models for all entities with Neon compatibility
3. **Shared Types** - TypeScript/Python types used across components
4. **Mock Data Generators** - Realistic test data for all entities
5. **Monorepo Structure** - Vercel-ready project setup
6. **GitHub Integration Contracts** - API contracts for repository operations

## Knowledge Gaps & Questions

I need to gather specific requirements before implementing Sprint 0. you should THINK DEEPLY and then ask me these questions one at a time including your suggestion based on our project info in CLAUDE.md, use my answers to construct a SPRINT0_SPEC.md.

### Question 1: Database Schema Design

For the core entities with Neon serverless PostgreSQL, which schema structure should we use?

**A) Minimal Schema (Recommended)**
```python
- User (id, clerk_id, email, name, created_at, updated_at)
- Project (id, name, user_id, github_repo_url, api_key, created_at)
- Document (id, project_id, file_path, content, summary, commit_hash, created_at, updated_at)
- SearchIndex (id, document_id, content_vector, full_text)
- Usage (id, project_id, timestamp, operation_type, tokens_used, cost)
```

**B) Extended Schema**
```python
- User (+ settings_json, clerk_org_id, last_seen)
- Project (+ description, visibility, settings_json, branch_name, include_patterns, exclude_patterns)
- Document (+ version, language, imports, exports, references)
- SearchIndex (+ relevance_scores, metadata_json)
- Usage (+ llm_model, endpoint_called, response_time)
- ApiKey (id, project_id, key_hash, name, created_at, last_used)
```

**C) Full Feature Schema**
```python
All of B plus:
- DocumentVersion (track all changes with git integration)
- Template (custom documentation templates per project)
- ProjectCollaborator (shared projects via Clerk orgs)
- WebhookLog (Clerk webhook history)
- GitHubToken (encrypted OAuth tokens for repo access)
```

Please select: **[A]**, [B], or [C]

---

### Question 2: API Endpoint Structure

Which API structure should we implement for Vercel Functions?

**A) RESTful CRUD (Recommended)**
```
# Clerk Webhooks
/api/webhooks/clerk (POST)

# Auth endpoints
/api/v1/auth/session (GET)
/api/v1/auth/logout (POST)

# Core endpoints
/api/v1/projects (GET, POST)
/api/v1/projects/{id} (GET, PUT, DELETE)
/api/v1/projects/{id}/documents (GET, POST)
/api/v1/projects/{id}/search (POST)
/api/v1/projects/{id}/api-keys (GET, POST, DELETE)

# User endpoints
/api/v1/user/profile (GET, PUT)
/api/v1/user/usage (GET)

# GitHub integration
/api/v1/github/repos (GET)
/api/v1/github/repos/{owner}/{repo}/files (GET, PUT)
```

**B) Function-Based (Vercel-style)**
```
/api/auth-session
/api/clerk-webhook
/api/create-project
/api/list-projects
/api/get-project
/api/search-documents
/api/generate-documentation
/api/sync-github
```

**C) Mixed Approach**
```
RESTful for CRUD operations
Function-based for complex operations
/api/v1/resources/* (REST)
/api/actions/* (Functions)
```

Please select: **[A]**, [B], or [C]

---

### Question 3: Clerk Integration Depth

How should we integrate Clerk authentication?

**A) Basic Integration (Recommended)**
```typescript
- Webhook endpoint for user sync (create/update/delete)
- Middleware to validate Clerk session tokens
- Store clerk_id in User table
- Use Clerk's session for all auth
```

**B) Advanced Integration**
```typescript
- All of A plus:
- Sync Clerk organizations to project permissions
- Use Clerk metadata for user preferences
- Implement Clerk's client SDK in frontend
- Role-based access with Clerk roles
```

**C) Minimal Integration**
```typescript
- Just webhook for user creation
- Manual session validation
- No organization support
```

Please select: **[A]**, [B], or [C]

---

### Question 4: MCP Server Communication

How should the MCP server communicate with the backend in a serverless environment?

**A) Direct Database Access (Recommended)**
```python
- MCP server connects directly to Neon
- Shared SQLAlchemy models
- Connection pooling per function
- No backend API calls needed
```

**B) HTTP API Calls**
```python
- MCP → Backend via HTTP
- API key authentication
- Retry logic for serverless cold starts
- Higher latency but cleaner separation
```

**C) Hybrid Approach**
```python
- Direct DB for reads (search/fetch)
- HTTP API for writes (usage tracking)
- Best performance with audit trail
```

Please select: **[A]**, [B], or [C]

---

### Question 5: GitHub Integration Approach

How should we handle GitHub repository access?

**A) GitHub App (Recommended)**
```typescript
- Create GitHub App for COGENT
- OAuth flow for installation
- App-level permissions for repo access
- Webhook support ready for future
```

**B) Personal Access Tokens**
```typescript
- Users provide PAT with repo scope
- Simpler implementation
- Store encrypted in database
- Less secure, more friction
```

**C) OAuth App**
```typescript
- Traditional OAuth flow
- User authorizes repo access
- Medium complexity
- Good user experience
```

Please select: **[A]**, [B], or [C]

---

### Question 6: Documentation Storage Strategy

Where should documentation files be stored in the repository?

**A) Configurable Location (Recommended)**
```
# User configures in settings:
- Default: .cogent/docs/{original_path}.md
- Alternative: alongside source files
- Custom: user-defined pattern
Example: src/auth.js → .cogent/docs/src/auth.md
```

**B) Fixed Alongside Files**
```
src/auth.js → src/auth.md
components/Button.tsx → components/Button.md
Always next to source files
```

**C) Single Documentation Directory**
```
All docs in /documentation/* 
Maintains source structure
Example: src/auth.js → /documentation/src/auth.md
```

Please select: **[A]**, [B], or [C]

---

### Question 7: Mock Data Complexity

What level of mock data should we generate for development?

**A) Realistic Mock Data (Recommended)**
```python
- 3 test users (with different Clerk IDs)
- 5 test projects with varied settings
- 50+ documents with actual code examples
- Usage data for past 30 days
- Realistic search scenarios
- GitHub repo integration examples
```

**B) Basic Mock Data**
```python
- 1 test user
- 2 test projects
- 10-20 simple documents
- Minimal usage data
- Basic search results
```

**C) Comprehensive Test Suite**
```python
- 10+ users with roles
- 20+ projects in various states
- 200+ documents across languages
- Full usage history
- Edge cases covered
```

Please select: **[A]**, [B], or [C]

---

## Implementation Instructions

Once we've answered these questions, you will proceed to:

1. Create the complete OpenAPI specification with Vercel Function constraints
2. Generate SQLAlchemy models optimized for Neon
3. Create shared TypeScript/Python types (with Clerk types)
4. Build mock data generators for all entities
5. Set up the monorepo structure with vercel.json
6. Define GitHub API integration contracts

ASK THESE QUESTIONS ONE AT A TIME IN ORDER. ASK ANY ADDITIONAL QUESTIONS YOU THINK NECESSARY.
