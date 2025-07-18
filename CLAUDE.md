# CLAUDE.md - COGENT (Code Organization and Generation Enhancement Tool)

## Overview

COGENT is a Claude Code (and eventually all coding agents) enhancement tool that forces Claude Code to generate and maintain comprehensive documentation for every code file it creates or modifies. It ensures that your codebase remains well-documented and understandable for both human developers and AI agents. It also supplies the exact context Claude Code needs to make new changes by searching these documents and inserting them into the context window.

## Development Best Practices

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
- **Test Before Deploy**: All PRs must pass CI/CD tests

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
- **API Documentation**: OpenAPI/Swagger for all endpoints
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
- **Database Indexes**: Optimize queries with proper indexing
- **Monitoring**: Track response times and resource usage

## Architecture

### System Components

1. **Monorepo Structure**
   - `/backend` - Go backend with PostgreSQL
   - `/frontend` - React + Vite web application  
   - `/mcp-server` - Model Context Protocol server
   - `/hooks` - Claude Code hook implementations
   - `/shared` - Shared types and utilities

2. **Backend Stack**
   - Language: Go
   - Database: PostgreSQL
   - Auth: OAuth 2.0 (GitHub, Google)
   - API: RESTful + WebSocket for real-time updates

3. **Frontend Stack**
   - Framework: React with Vite
   - UI: SHADCN Modern dashboard interface
   - State Management: TBD based on complexity

4. **MCP Server**
   - Searches documentation files
   - Validates relevance using LLMs
   - Injects context into Claude Code
   - Communicates with backend via API

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
   - Full-text PostgreSQL search
   - Vector embeddings for semantic matching
2. **Relevance Validation**: LLM validates search results
3. **Context Injection**: Relevant docs provided to Claude Code

### 3. Authentication & Security

- **Web App**: OAuth 2.0 (GitHub + Google)
- **MCP Server**: Per-project API keys
- **Documentation**: Configurable visibility per project

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

- Incremental updates on file modification
- Only changed sections updated
- Git handles version control
- No separate versioning system

## Language Support

### Phase 1 Languages
- JavaScript/TypeScript
- Python
- Go

### Documentation Adapters
- Language-specific parsing
- Framework detection (React, Django, etc.)
- Syntax-aware documentation

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

## Future Enhancements

- Cross-project documentation search
- Advanced analytics and insights
- Additional language support
- Custom documentation plugins
- Team collaboration features
- Documentation quality scoring
- AI-powered documentation suggestions
