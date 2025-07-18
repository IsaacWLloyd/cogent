# COGENT Backend API

Go-based backend service providing REST API endpoints for project management, documentation storage, user authentication, and billing integration.

## Architecture

- **Language**: Go 1.24+
- **Database**: PostgreSQL 17+
- **Cache**: Redis 7+
- **Auth**: OAuth 2.0 (GitHub, Google)
- **Payments**: Polar integration
- **LLM**: OpenRouter API

## Key Components

- `/cmd` - Application entry points and CLI tools
- `/internal` - Private application code
- `/pkg` - Exportable packages
- `/migrations` - Database schema migrations
- `/api` - API route handlers
- `/auth` - Authentication middleware
- `/models` - Database models
- `/services` - Business logic layer

## Development

```bash
# Start with Docker
make dev

# Local development
go mod download
go run main.go

# Run tests
go test ./...

# Run migrations
go run cmd/migrate/main.go
```

## API Endpoints

- `POST /auth/login` - OAuth login
- `GET /projects` - List user projects
- `POST /projects` - Create new project
- `GET /projects/{id}/docs` - Get project documentation
- `POST /search` - Search documentation
- `GET /usage` - Usage analytics

## Environment Variables

See `.env.example` for required configuration.

## Track Assignments

This component is assigned to **Track 3: Backend API Development**.