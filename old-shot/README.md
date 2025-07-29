# COGENT
**Code Organization and Generation Enhancement Tool**

Force Claude Code and other coding agents to generate and maintain comprehensive documentation for every code file they create or modify.

## Quick Start

```bash
# Install dependencies
npm run setup

# Start development servers
npm run dev
```

## Project Structure

```
cogent/
├── backend/          # FastAPI backend with PostgreSQL
├── frontend/         # React + TypeScript frontend
├── mcp-server/       # PydanticAI MCP server
├── hooks/            # Claude Code hooks
├── shared/           # Shared types and utilities
├── openapi.yaml      # API specification
└── PHASE0_SPEC.md    # Implementation specification
```

## Architecture

- **Backend**: FastAPI with SQLAlchemy, PostgreSQL/SQLite, OAuth authentication
- **Frontend**: React + Vite with SHADCN UI components
- **MCP Server**: PydanticAI-based documentation search and context injection
- **Documentation**: Stored alongside code files with git version control

## Development

Each component has its own README with specific setup instructions:
- [Backend](./backend/README.md)
- [Frontend](./frontend/README.md)
- [MCP Server](./mcp-server/README.md)
- [Hooks](./hooks/README.md)

## Environment Setup

1. Copy `.env.example` to `.env`
2. Configure OAuth providers (GitHub, Google)
3. Set OpenRouter API key for Gemini Flash
4. Configure database connection

## Sprint 0 Status

✅ **COMPLETED**: Foundation & Contracts
- Database schema (SQLAlchemy models)
- API specification (OpenAPI)
- Shared types (TypeScript + Python)
- Mock data generators
- Monorepo structure setup

Ready for parallel team development!
