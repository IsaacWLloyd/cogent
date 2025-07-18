# COGENT MCP Server

Model Context Protocol server that provides Claude Code with intelligent context injection by searching project documentation and validating relevance.

## Architecture

- **Language**: Go 1.24+
- **Protocol**: MCP (Model Context Protocol)
- **Search**: Hybrid full-text + semantic search
- **LLM**: OpenRouter for relevance validation
- **Communication**: Backend API integration

## Key Components

- `/cmd` - MCP server entry point
- `/internal/mcp` - MCP protocol implementation
- `/internal/search` - Search engine logic
- `/internal/relevance` - LLM-based relevance validation
- `/pkg/client` - Backend API client

## MCP Tools Provided

### `search_documentation`
Searches project documentation using hybrid search.

**Input:**
- `project_id` - Target project identifier
- `query` - Search query string
- `file_types` - Optional file type filters
- `max_results` - Maximum results to return

**Output:**
- Ranked search results with relevance scores
- File paths and content snippets
- Line number references

### `get_context`
Retrieves and validates relevant context for Claude Code.

**Input:**
- `project_id` - Target project
- `current_file` - File being edited (optional)
- `query` - Context request query
- `max_tokens` - Token budget for context

**Output:**
- Filtered, relevant context
- Source attributions
- Token usage information

### `validate_relevance`
Uses LLM to validate search result relevance.

**Input:**
- `query` - Original search query
- `results` - Search results to validate

**Output:**
- Filtered results above relevance threshold
- Reasoning for filtering decisions

## Search Strategy

1. **Full-text Search**: PostgreSQL full-text search
2. **Semantic Search**: Vector embeddings for meaning
3. **Relevance Validation**: LLM-based filtering
4. **Context Assembly**: Token-aware result compilation

## Development

```bash
# Start with Docker
make dev

# Local development
go mod download
go run main.go

# Run tests
go test ./...
```

## Configuration

- Backend API URL for documentation retrieval
- OpenRouter API key for LLM calls
- MCP protocol settings
- Search ranking parameters

## Integration

The MCP server is designed to be called by Claude Code via the MCP protocol. It communicates with the backend API to retrieve documentation and uses LLMs to ensure relevance.

## Track Assignments

This component is assigned to **Track 2: MCP Server Development**.