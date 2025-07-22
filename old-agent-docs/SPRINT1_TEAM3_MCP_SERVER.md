# Sprint 1 Team 3: MCP Server Implementation

## Project Context

You are working on **COGENT** (Code Organization and Generation Enhancement Tool), a comprehensive documentation system that forces Claude Code to generate and maintain documentation for every code file it creates or modifies.

**Sprint 0 has been completed** and established all foundational contracts:
- Complete OpenAPI specification (`openapi.yaml`) defining the backend API
- SQLAlchemy database models (`backend/models.py`)
- Shared TypeScript and Python types (`shared/types.ts`, `shared/models.py`)
- PydanticAI dependencies configured (`mcp-server/requirements.txt`)

## Your Team's Responsibilities

As the **MCP Server** team, you are responsible for implementing the PydanticAI-based Model Context Protocol server that acts as the bridge between Claude Code and the COGENT backend. This is a critical component that provides intelligent documentation search and context injection capabilities.

### Core Components to Build

**PydanticAI Agent Architecture**
- Documentation search agent with type-safe Pydantic models
- Relevance validation agent to score search results
- Tool definitions for `search_documentation` and `validate_relevance`
- Error handling and validation with Pydantic schemas

**MCP Protocol Implementation**  
- Stdio transport for local development and testing
- HTTP/SSE transport for production deployments
- Tool registration with clear schemas and descriptions
- State management for stateful MCP connections

**Backend API Integration**
- HTTP client for communicating with FastAPI backend
- Authentication using project API keys
- Exponential backoff retry logic for reliability
- Request/response validation using shared Pydantic models

**Context Processing**
- Document content analysis and chunking
- Relevance scoring using LLM validation
- Context injection formatting for Claude Code
- Search result ranking and filtering

## Available Resources

You have access to these completed Sprint 0 deliverables:

1. **Shared Pydantic Models** (`shared/models.py`): Type-safe models for User, Project, Document, SearchRequest, and SearchResult
2. **OpenAPI Specification** (`openapi.yaml`): Backend API contracts for search endpoints
3. **Requirements** (`mcp-server/requirements.txt`): PydanticAI, HTTPX, and other dependencies
4. **CLAUDE.md**: Comprehensive documentation of how the MCP server fits into the overall architecture

## Technology Stack

- **Framework**: PydanticAI for agent-based architecture
- **Protocol**: Model Context Protocol (MCP) with stdio and HTTP/SSE transports
- **HTTP Client**: HTTPX for async backend communication
- **Validation**: Pydantic v2 for all data structures
- **LLM Provider**: Gemini Flash via OpenRouter (configured via environment variables)
- **Testing**: Pytest with asyncio support
- **Code Quality**: Ruff for linting

## MCP Server Architecture

Based on CLAUDE.md, your MCP server should implement this flow:

1. **Claude Code Search Request** → MCP Server receives search query
2. **Backend API Call** → Query FastAPI `/projects/{id}/search` endpoint  
3. **Relevance Validation** → PydanticAI agent validates each result in parallel
4. **Context Injection** → Return formatted, relevant documentation to Claude Code

## Knowledge Gaps & Questions

Before writing your detailed implementation specification, I need you to research the existing codebase and ask me specific questions about these areas where you need clarification:

### 1. PydanticAI Agent Architecture
- What should be our agent composition strategy (single agent vs multiple specialized agents)?
- How should we structure the agent system prompts for documentation search vs relevance validation?
- What Pydantic models do we need for agent inputs, outputs, and intermediate processing?
- How should we handle agent lifecycle and resource cleanup?

### 2. MCP Protocol Implementation
- Which transport mechanism should we prioritize for initial development (stdio vs HTTP/SSE)?
- How should we structure our tool definitions and schemas for Claude Code integration?
- What's our strategy for handling MCP connection state and reconnection logic?
- How should we implement proper error handling and graceful degradation?

### 3. Backend API Integration
- How should we handle API authentication and key validation?
- What's our retry strategy for network failures and rate limiting?
- How should we structure the HTTP client for optimal performance?
- What caching strategy should we implement for repeated searches?

### 4. Search and Relevance Logic
- What criteria should the relevance validation agent use to score search results?
- How should we handle different types of documentation content (code comments, markdown files, etc.)?
- What's our strategy for handling large documents that need to be chunked?
- How should we rank and filter results before returning to Claude Code?

### 5. Configuration Management
- How should we handle environment variables and configuration files?
- What's our strategy for development vs production configuration?
- How should we manage API keys and secrets securely?
- What logging and monitoring should we implement?

### 6. Error Handling & Validation
- What specific error types should we handle from the backend API?
- How should we validate search queries and responses?
- What's our strategy for handling malformed or missing documentation?
- How should we communicate errors back to Claude Code?

### 7. Performance & Optimization
- What's our strategy for concurrent relevance validation of multiple search results?
- How should we handle timeouts and async operations?
- What caching mechanisms should we implement?
- How should we optimize for Claude Code's context window limitations?

### 8. Development & Testing
- How should we mock the backend API for isolated MCP server testing?
- What's our strategy for testing the PydanticAI agents in isolation?
- How should we test the MCP protocol implementation?
- What integration testing approach should we use with Claude Code?

### 9. Integration Points
- How exactly will Claude Code discover and connect to our MCP server?
- What's the expected request/response format for the search tool?
- How should we handle project-specific configurations and API keys?
- What's our strategy for handling multiple concurrent Claude Code sessions?

## Your Task

1. **Research Phase**: Examine the existing Sprint 0 deliverables, especially the shared Pydantic models and OpenAPI specification
2. **Question Phase**: Ask me specific, focused questions about the knowledge gaps above, one area at a time
3. **Specification Phase**: Once all gaps are filled, write a comprehensive implementation specification that includes:
   - Detailed PydanticAI agent architecture with type-safe models
   - Complete MCP protocol implementation (stdio and HTTP/SSE)
   - Backend API integration with authentication and error handling
   - Search and relevance validation logic
   - Configuration and deployment strategy
   - Testing approach with mock backend integration
   - Performance optimization strategies

## Directory Restrictions

**CRITICAL: You are STRICTLY LIMITED to working within these directories:**
- `/mcp-server/` - All PydanticAI MCP server code
- `/shared/` - Only for reading shared Python types, NO modifications allowed

**FORBIDDEN DIRECTORIES:**
- `/backend/` - Assigned to Team 1
- `/frontend/` - Assigned to Team 2
- `/hooks/` - Will be handled separately
- Any other directories not explicitly listed above

**File Creation Rules:**
- Create new files ONLY within `/mcp-server/`
- Read existing files in `/shared/` for Pydantic models but DO NOT modify them
- If you need changes to shared types, ask for approval first
- Modify `/mcp-server/requirements.txt` as needed for dependencies

## Git Commit Guidelines

**Commit Strategy - Logical, Atomic Commits:**
1. **One Feature Per Commit** - Each commit should represent one complete, working feature
2. **Commit Early and Often** - Don't wait until everything is done
3. **Meaningful Messages** - Use conventional commit format

**Required Commit Pattern:**
```
feat(mcp): add PydanticAI agent for documentation search
feat(mcp): implement MCP protocol with stdio transport
feat(mcp): add backend API client with authentication
test(mcp): add unit tests for search relevance validation
fix(mcp): resolve MCP connection timeout issues
```

**Commit Frequency Guidelines:**
- After setting up basic PydanticAI agent structure
- After implementing MCP protocol transport (stdio)
- After implementing backend API client integration
- After adding search and relevance validation tools
- After implementing error handling and retry logic
- After adding HTTP/SSE transport support
- After writing tests for each component
- Before integration testing with Claude Code

**Each commit must:**
- Pass all Python type checking (mypy/ruff)
- Include relevant test coverage for new code
- Have working, testable MCP server functionality
- Include clear commit message explaining the change
- Follow PydanticAI best practices and patterns

Remember: Your MCP server is the critical bridge between Claude Code and the COGENT backend. It must be reliable, performant, and provide accurate context to enable Claude Code to make informed documentation decisions.

**Start by asking me your first set of questions about the PydanticAI agent architecture.**