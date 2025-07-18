# COGENT Shared Types and Utilities

Common Go types, TypeScript interfaces, and utility functions shared across all COGENT components.

## Architecture

This package provides the foundational types and contracts that enable communication between:
- Backend API server
- MCP server
- Hook system utilities
- Frontend application (via TypeScript types)

## Key Components

### Go Types (`types.go`)
- `Project` - Project configuration and metadata
- `User` - User account information
- `Documentation` - Generated documentation records
- `HookEvent` - Hook system event structures
- `Usage` - Billing and usage tracking

### MCP Types (`mcp.go`)
- `MCPToolDefinition` - MCP protocol tool definitions
- `MCPSearchRequest/Response` - Search API contracts
- `ContextRequest/Response` - Context injection contracts
- `RelevanceValidation` - LLM relevance validation

### TypeScript Types (`../frontend/src/types/`)
- Mirror Go types for frontend consumption
- Additional UI-specific types
- API response wrappers

## Type Definitions

### Core Entities
```go
type Project struct {
    ID       string        `json:"id"`
    Name     string        `json:"name"`
    Path     string        `json:"path"`
    UserID   string        `json:"user_id"`
    Config   ProjectConfig `json:"config"`
}
```

### Configuration
```go
type ProjectConfig struct {
    IncludePatterns    []string           `json:"include_patterns"`
    ExcludePatterns    []string           `json:"exclude_patterns"`
    DocumentationStyle DocumentationStyle `json:"documentation_style"`
    Visibility         ProjectVisibility  `json:"visibility"`
}
```

### Search & Context
```go
type MCPSearchRequest struct {
    ProjectID  string   `json:"project_id"`
    Query      string   `json:"query"`
    FileTypes  []string `json:"file_types,omitempty"`
    MaxResults int      `json:"max_results,omitempty"`
}
```

## Usage

### In Go Components
```go
import "github.com/cogent/shared"

func processProject(p shared.Project) {
    // Use shared types
}
```

### In Frontend
```typescript
import { Project, User } from "@/types";

const project: Project = {
    id: "123",
    name: "My Project",
    // ...
};
```

## Versioning

Shared types follow semantic versioning:
- **Major**: Breaking changes to existing types
- **Minor**: New types or optional fields
- **Patch**: Bug fixes or documentation

All components must use compatible versions of shared types.

## Development

```bash
# Validate Go types
go mod tidy
go build

# Generate TypeScript types (if automated)
go run tools/generate-ts-types.go
```

## Cross-Component Contracts

This package serves as the **single source of truth** for data structures used across:

1. **API Contracts**: Request/response types between frontend and backend
2. **Database Models**: Consistent field names and types
3. **MCP Protocol**: Tool definitions and message formats
4. **Hook Events**: Standardized event structures
5. **Configuration**: Shared configuration schemas

## Track Dependencies

All development tracks depend on this shared foundation:
- **Track 1**: Hook event types
- **Track 2**: MCP protocol types  
- **Track 3**: API and database types
- **Track 4**: Frontend TypeScript types
- **Track 5**: Usage and billing types