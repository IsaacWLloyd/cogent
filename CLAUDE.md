# CLAUDE.md - COGENT (Code Organization and Generation Enhancement Tool)

## Overview

COGENT is a Claude Code (and eventually all coding agents) enhancement tool that forces Claude Code to generate and maintain comprehensive documentation for every code file it creates or modifies. It ensures that your codebase remains well-documented and understandable for both human developers and AI agents. It also supplies the exact context Claude Code needs to make new changes by searching these documents and inserting them into the context window.

## Development Best Practices

### questions.
- if you are working and come across something you are unsure about ask for my input before continuing

### Code Organization
- **Modularity First**: Keep components small, focused, and reusable
- **Clear Separation**: Maintain strict boundaries between backend, frontend, and MCP layers
- **Shared Types**: Use the `/shared` directory for cross-component types and utilities
- **Single Responsibility**: Each module/function should do one thing well

### Testing Strategy
- **Test Coverage**: Aim for 80%+ coverage on critical paths
- **Unit Tests**: Test individual functions and components in isolation
- **Integration Tests**: Test API endpoints and component interactions
- **E2E Tests**: Test critical user flows (auth, documentation generation, search)

### Version Control
- **Atomic Commits**: Each commit should represent one logical change
- **Descriptive Messages**: Use conventional commits format (feat:, fix:, docs:, etc.)
- **Branch Strategy**: 
  - `main` - stable production code
  - `develop` - integration branch
  - `feature/*` - new features
  - `fix/*` - bug fixes
- **PR Reviews**: All code requires review before merging

### Documentation
- **Code Comments**: Explain WHY, not WHAT
- **API Documentation**: FastAPI automatic OpenAPI/Swagger generation
- **README Files**: Each major directory should have its own README
- **Architecture Decisions**: Document major decisions in ADRs (Architecture Decision Records)

### Error Handling
- **Fail Gracefully**: Never crash the entire system
- **Meaningful Errors**: Provide actionable error messages
- **Logging Levels**: Use appropriate log levels (ERROR, WARN, INFO, DEBUG)
- **User-Friendly Messages**: Translate technical errors for end users

### Security
- **Environment Variables**: Never commit secrets
- **Input Validation**: Validate all user inputs
- **Rate Limiting**: Implement on all API endpoints

### Performance
Don't worry about this until later 
- **Lazy Loading**: Load resources only when needed
- **Caching Strategy**: Cache expensive operations (searches, LLM calls)
- **Database Indexes**: SQLAlchemy query optimization with proper indexing
- **Async Operations**: FastAPI async/await for non-blocking operations
- **Monitoring**: Track response times and resource usage

## Architecture

### System Components

1. **Monorepo Structure**
   - `/backend` - Python FastAPI backend with SQLAlchemy
   - `/frontend` - React + Vite web application  
   - `/mcp-server` - PydanticAI Model Context Protocol server
   - `/hooks` - Claude Code hook implementations
   - `/shared` - Shared types and utilities

2. **Backend Stack**
   - Language: Python with FastAPI
   - Database: SQLAlchemy (PostgreSQL for production, SQLite for development)
   - Auth: FastAPI OAuth2 with JWT tokens (GitHub, Google)
   - API: RESTful with automatic OpenAPI documentation

3. **Frontend Stack**
   - Framework: React with Vite
   - UI: SHADCN Modern dashboard interface
   - State Management: TBD based on complexity

4. **MCP Server (PydanticAI)**
   - Standalone Python module using PydanticAI framework
   - Searches documentation files with type-safe operations
   - Validates relevance using LLMs with Pydantic models
   - Injects context into Claude Code via MCP protocol
   - Communicates with FastAPI backend via HTTP API
   - Supports stdio and HTTP/SSE transport mechanisms

## How COGENT Works

### 1. Documentation Generation Flow

1. **Hook Trigger**: PostToolUse hook fires after file modifications (Edit, Write, MultiEdit)
2. **Synchronous Summary**: Claude Code must write:
   - Brief summary of changes
   - Purpose of the code
   - Connections to other files
3. **Async Completion**: Subagent spawned via Task tool to:
   - Complete detailed documentation
   - Validate docs match code
   - Update cross-references
   - Handle all related documentation tasks

### 2. Context Retrieval Flow

1. **Search Phase**: Hybrid search using:
   - Full-text SQLAlchemy search with PostgreSQL
   - Vector embeddings for semantic matching
2. **Relevance Validation**: PydanticAI agent validates search results with type-safe models. more specifically we ask 1 agent per potential match if it believes it is the right place for Claude COde to make changes. In parallel
3. **Context Injection**: Relevant docs provided to Claude Code via MCP protocol

### 3. Authentication & Security

- **Web App**: FastAPI OAuth2 with JWT tokens (GitHub + Google)
- **MCP Server**: Per-project API keys with secure token validation
- **Documentation**: Configurable visibility per project. Users can choose wether the documents are in there git repo

## Payment Model

- **Usage-Based Pricing**: 
  - Meter OpenRouter API usage for LLM calls
  - Charge usage + margin
  - Integrated with Polar for payments
- **Rate Limiting**: Per-project limits

## Web Application

### Main Features

1. **Dashboard View**
   - Shows most recently accessed project on login
   - Project list with quick access
   - Documentation search interface
   - Usage analytics and billing

2. **Project Management**
   - View/search project documentation
   - Configure documentation settings
   - Set visibility (public/private)
   - Include/exclude file patterns

3. **Settings Interface**
   - Project-specific configurations
   - Documentation template customization
   - API key management
   - Usage monitoring

### User Flow

1. **Onboarding**: Run install script in repo → OAuth prompt → Project setup
2. **Daily Use**: Access via web dashboard → Search docs → Configure settings
3. **Integration**: MCP server uses project API key → Retrieves relevant context

## Hook Implementation

### Claude Code Integration

```json
{
  "hooks": {
    "postToolUse": {
      "command": "cogent-hook post-tool-use",
      "tools": ["Edit", "Write", "MultiEdit"],
      "timeout": 30000
    }
  }
}
```

### Hook Behavior

1. **Detects file changes** via PostToolUse event
2. **Blocks until summary written** (synchronous)
3. **Spawns subagent** for detailed documentation
4. **Returns success** allowing Claude to continue
5. **Warns on failure** but doesn't block code changes

### Future Compatibility

- Hook system designed to be agent-agnostic
- Adapter pattern for other coding agents
- Standardized documentation format

## Documentation Standards

### File Organization

- Documentation files stored alongside code files
- Example: `auth.js` → `auth.md` in same directory
- Module-level docs for feature groups

### Template Structure

- Customizable per project via dashboard
- Default template includes:
  - File purpose and overview
  - Key functions/classes
  - Dependencies and imports
  - Related files and connections
  - Usage examples
  - Change history summary

### Update Strategy

- Incremental documentation updates on file modification
- Only changed sections updated
- Git handles version control
- No separate versioning system
- because of branching in git we need to make the state of the project in the dashboard be tied to a commit in github. you should be able to view past commits or other branches easily. under the hood its connected by commit hash tho.

## Language Support

### Phase 1 Languages
- JavaScript/TypeScript
- Python

## Installation

```bash
# Run in your project root
curl -sSL https://usecogent.io/install | bash

# Follow OAuth prompts
# Configure project settings
```

## Configuration

### Project-Level Settings
- Stored in `.cogent/config.json`
- Managed via web dashboard
- Include/exclude patterns
- Documentation templates
- Visibility settings

### Global Settings
- User preferences on usecogent.io
- Default templates
- API key management
- Billing preferences

## Error Handling

- Documentation failures warn but don't block
- Placeholder docs created on errors  
- Retry logic for transient failures
- Error details logged for debugging

## Security Considerations

- API keys scoped per project
- OAuth tokens for web access
- Documentation visibility controls
- No secrets in documentation
- Secure hook execution environment

## PydanticAI Best Practices

### MCP Server Implementation
- **Type Safety**: Use Pydantic models for all data validation and serialization
- **Agent Architecture**: Structure agents with clear tool definitions and result validation
- **Transport Selection**: 
  - Use `stdio` transport for local development and testing
  - Use `HTTP/SSE` transport for production deployments
- **Error Handling**: Implement robust error handling with Pydantic validation errors
- **Resource Management**: Properly manage agent lifecycle and cleanup

### Integration Patterns
- **Modular Design**: Keep MCP server separate from FastAPI backend for flexibility
- **API Communication**: Use typed HTTP clients for backend communication
- **Context Validation**: Validate retrieved documentation context before injection
- **Tool Registration**: Register tools with clear schemas and documentation
- **State Management**: Handle stateful MCP connections properly

### Documentation Links
- [PydanticAI Documentation](https://ai.pydantic.dev/)
- [MCP Overview](https://ai.pydantic.dev/mcp/)
- [MCP Server Implementation](https://ai.pydantic.dev/mcp/server/)
- [MCP Client Usage](https://ai.pydantic.dev/mcp/client/)
- [Agent Architecture Guide](https://ai.pydantic.dev/agents/)
- [Type Safety with Pydantic](https://docs.pydantic.dev/latest/)

### Code Examples

```python
# MCP Server with PydanticAI
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic import BaseModel

class DocumentationQuery(BaseModel):
    query: str
    project_id: str
    max_results: int = 10

class DocumentationResult(BaseModel):
    content: str
    file_path: str
    relevance_score: float

# Agent for documentation search and validation
documentation_agent = Agent(
    model='openai:gpt-4',
    result_type=list[DocumentationResult],
    system_prompt='You are a documentation search and relevance validation agent.'
)
```
## Github connection

- we need to connect to github for it to work because we are storing documentation in the users repos.

## Future Enhancements

- Cross-project documentation search
- Advanced analytics and insights
- Additional language support
- Custom documentation plugins
- Team collaboration features
- Documentation quality scoring
- AI-powered documentation suggestions
