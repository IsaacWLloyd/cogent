# Backend Implementation Notes

## Future Implementation Tasks

### Security & Production Readiness
- **PostgreSQL Connection Parameters**: Add SSL, timeouts, and connection security configurations
- **Rate Limiting**: Implement rate limiting middleware (429 responses already structured)
- **Log Redaction**: Redact sensitive data (API keys, emails, tokens) from logs in production
- **Error Message Sanitization**: Replace specific API key validation errors with generic messages for security

### API Key Authentication
- **MCP Server Authentication**: Implement proper API key validation against `Project.api_key` field
- **API Key Dependency**: Create `verify_api_key()` dependency function for MCP endpoints
- **API Key Error Handling**: Determine whether to use 401 vs 403 for invalid API keys

### Performance & Scalability
- **Database Connection Pooling**: Current settings are basic, may need tuning for production load
- **Search Index Population**: Implement automatic vector embedding generation when Team 4 delivers search functionality
- **Caching Strategy**: Add caching for read-heavy operations (user profiles, project lists)

### API Enhancements
- **Background Task System**: Evaluate if any operations need async processing
- **Request/Response Compression**: Add gzip middleware for large document payloads
- **API Versioning**: Current `/api/v1` prefix supports versioning, but no strategy defined yet

### Monitoring & Observability
- **Request Correlation IDs**: Currently implemented, but need log aggregation strategy
- **Health Checks**: Add `/health` endpoint for deployment monitoring
- **Metrics Collection**: Add Prometheus/StatsD metrics for key operations

### Testing & Quality
- **Integration Tests**: Current tests are unit-focused, need API integration tests
- **Load Testing**: No performance benchmarks established
- **Mock Data Expansion**: Current mock data is basic, may need more realistic scenarios

## Implementation Decisions Made

### Database
- SQLite for development (default), PostgreSQL for production
- Nullable vector fields with graceful fallback to full-text search
- Alembic migrations in `/backend/migrations/`
- FastAPI dependency injection for database sessions

### Authentication
- Real JWT with proper signing and claims (iat, jti, exp)
- httpOnly cookies with SameSite=Lax protection
- Mock implementation uses consistent test users from mock_data.py
- No API key validation in Sprint 1 (defer to later)

### Error Handling
- 422 for validation errors, 409 for conflicts, 429 structure for rate limiting
- Full stack traces in development, sanitized messages in production
- Generic HTTP exceptions (no custom exception classes)
- Comprehensive request/response logging with correlation IDs

### API Patterns
- Consistent response envelope with metadata
- Offset/limit pagination with sensible defaults
- OpenAPI camelCase naming with Pydantic conversion
- Synchronous document creation (Claude Code responsibility)
- Path validation with directory traversal protection