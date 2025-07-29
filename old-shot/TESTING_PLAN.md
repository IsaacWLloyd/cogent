# COGENT Testing Strategy & Implementation Plan

## Overview
Comprehensive testing strategy to ensure 80%+ coverage on critical paths and provide reliable foundation for all teams.

## Testing Architecture

### 1. Backend Testing (Python/FastAPI)

#### Test Structure
```
tests/
├── unit/                   # Unit tests for individual functions
│   ├── test_models.py     # SQLAlchemy model validation
│   ├── test_auth.py       # Authentication logic
│   ├── test_github.py     # GitHub integration
│   └── test_utils.py      # Utility functions
├── integration/           # API endpoint testing
│   ├── test_projects.py   # Project CRUD operations
│   ├── test_documents.py  # Document operations
│   ├── test_search.py     # Search functionality
│   └── test_webhooks.py   # Clerk/GitHub webhooks
├── e2e/                   # End-to-end user flows
│   ├── test_user_flow.py  # Complete user journey
│   └── test_mcp_flow.py   # MCP server integration
└── fixtures/              # Test data and fixtures
    ├── conftest.py        # Pytest configuration
    ├── database.py        # Test database setup
    └── mock_data.py       # Test data factories
```

#### Test Framework Stack
- **pytest**: Main testing framework
- **pytest-asyncio**: Async test support
- **httpx**: HTTP client for API testing
- **factory-boy**: Test data generation
- **pytest-mock**: Mocking utilities
- **pytest-cov**: Coverage reporting
- **sqlalchemy-utils**: Database test utilities

#### Key Test Categories
1. **Model Tests**: Validation, relationships, constraints
2. **API Tests**: All endpoints, authentication, error handling
3. **Integration Tests**: Database operations, external APIs
4. **Security Tests**: Authentication, authorization, input validation
5. **Performance Tests**: Database queries, API response times

### 2. Frontend Testing (React/TypeScript)

#### Test Structure
```
frontend/src/
├── __tests__/             # Test files
│   ├── components/        # Component tests
│   ├── hooks/             # Custom hook tests
│   ├── services/          # API client tests
│   └── utils/             # Utility function tests
├── __mocks__/             # Mock implementations
│   ├── api.ts            # Mock API responses
│   └── clerk.ts          # Mock Clerk SDK
└── test-utils/            # Testing utilities
    ├── render.tsx         # Custom render with providers
    └── server.ts          # MSW mock server
```

#### Test Framework Stack
- **Vitest**: Fast test runner (Vite-native)
- **React Testing Library**: Component testing
- **MSW**: API mocking
- **@testing-library/jest-dom**: DOM assertions
- **@testing-library/user-event**: User interaction simulation

#### Key Test Categories
1. **Component Tests**: Rendering, props, user interactions
2. **Hook Tests**: Custom hooks, state management
3. **Integration Tests**: API client, authentication flows
4. **E2E Tests**: Critical user journeys (via Playwright)

### 3. MCP Server Testing (PydanticAI)

#### Test Structure
```
mcp/tests/
├── test_agents.py         # PydanticAI agent testing
├── test_tools.py          # MCP tool testing
├── test_search.py         # Document search testing
├── test_relevance.py      # Relevance validation testing
└── test_integration.py    # Claude Code integration
```

#### Test Framework Stack
- **pytest**: Main framework
- **pydantic-ai-test**: PydanticAI testing utilities
- **pytest-asyncio**: Async support
- **httpx**: API client testing

### 4. Database & Search Testing

#### Test Categories
1. **Migration Tests**: Schema changes, data integrity
2. **Query Performance**: Index usage, query optimization
3. **Search Tests**: Full-text search, vector search accuracy
4. **Connection Tests**: Serverless connection handling

## Implementation Plan

### Phase 1: Foundation Setup (2-3 hours)
1. **Test Environment Configuration**
   - Set up pytest with asyncio support
   - Configure test database (SQLite for speed)
   - Set up coverage reporting
   - Create mock data factories

2. **CI/CD Integration**
   - GitHub Actions workflow for automated testing
   - Coverage reporting with codecov
   - Test matrix (Python 3.11, Node.js 18/20)

### Phase 2: Backend Core Tests (4-5 hours)
1. **Model Testing**
   - All SQLAlchemy models
   - Relationships and constraints
   - Validation logic

2. **API Endpoint Testing**
   - All CRUD operations
   - Authentication flows
   - Error handling scenarios
   - Input validation

3. **Integration Testing**
   - Database operations
   - Clerk webhook handling
   - GitHub API integration

### Phase 3: Frontend Tests (3-4 hours)
1. **Component Testing**
   - Key UI components
   - Form validation
   - Authentication components

2. **Service Testing**
   - API client functions
   - Error handling
   - Authentication state management

### Phase 4: MCP & Search Tests (2-3 hours)
1. **MCP Server Testing**
   - Document search functionality
   - Relevance validation
   - API authentication

2. **Search Testing**
   - Full-text search accuracy
   - Vector search performance
   - Query optimization

### Phase 5: E2E & Performance (2-3 hours)
1. **End-to-End Tests**
   - Complete user flows
   - Cross-system integration
   - Error scenarios

2. **Performance Testing**
   - API response times
   - Database query performance
   - Memory usage patterns

## Test Coverage Goals

### Critical Path Coverage (Must be 90%+)
- User authentication and session management
- Project CRUD operations
- Document generation and storage
- Search functionality (both full-text and vector)
- API key management
- GitHub integration
- MCP server document retrieval

### Standard Coverage (Target 80%+)
- Utility functions
- Data validation
- Error handling
- Webhook processing
- UI components

### Lower Priority Coverage (Target 60%+)
- Edge case handling
- Performance optimizations
- Logging and monitoring

## Test Data Strategy

### Mock Data Approach
1. **Factory Pattern**: Use factory-boy for consistent test data
2. **Fixtures**: Pytest fixtures for common test scenarios
3. **Isolated Tests**: Each test gets fresh data
4. **Realistic Data**: Based on actual usage patterns

### Test Database Strategy
1. **Unit Tests**: SQLite in-memory for speed
2. **Integration Tests**: PostgreSQL test database
3. **E2E Tests**: Full test environment with seeded data

## Sample Test Implementation

### Backend API Test Example
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.factories import UserFactory, ProjectFactory

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_project_success(authenticated_user):
    """Test successful project creation"""
    project_data = {
        "name": "Test Project",
        "github_repo_url": "https://github.com/user/repo",
        "description": "Test description"
    }
    
    response = client.post(
        "/api/v1/projects",
        json=project_data,
        headers={"Authorization": f"Bearer {authenticated_user.token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == project_data["name"]
    assert data["user_id"] == authenticated_user.id

@pytest.mark.asyncio
async def test_create_project_invalid_repo(authenticated_user):
    """Test project creation with invalid repository URL"""
    project_data = {
        "name": "Test Project",
        "github_repo_url": "invalid-url"
    }
    
    response = client.post(
        "/api/v1/projects",
        json=project_data,
        headers={"Authorization": f"Bearer {authenticated_user.token}"}
    )
    
    assert response.status_code == 400
    assert "github_repo_url" in response.json()["details"]
```

### Frontend Component Test Example
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { ProjectForm } from '@/components/ProjectForm'
import { mockApiClient } from '@/__mocks__/api'

describe('ProjectForm', () => {
  test('creates project successfully', async () => {
    const onSuccess = jest.fn()
    
    render(<ProjectForm onSuccess={onSuccess} />)
    
    fireEvent.change(screen.getByLabelText(/project name/i), {
      target: { value: 'Test Project' }
    })
    
    fireEvent.change(screen.getByLabelText(/repository url/i), {
      target: { value: 'https://github.com/user/repo' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: /create project/i }))
    
    await waitFor(() => {
      expect(mockApiClient.createProject).toHaveBeenCalledWith({
        name: 'Test Project',
        github_repo_url: 'https://github.com/user/repo'
      })
      expect(onSuccess).toHaveBeenCalled()
    })
  })
})
```

## Continuous Integration

### GitHub Actions Workflow
```yaml
name: Test Suite
on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg15
        env:
          POSTGRES_PASSWORD: postgres
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt pytest-cov
      - name: Run tests
        run: pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install dependencies
        run: cd frontend && npm install
      - name: Run tests
        run: cd frontend && npm run test:coverage
```

## Success Criteria

### Test Quality Metrics
- ✅ 90%+ coverage on critical paths
- ✅ 80%+ overall coverage
- ✅ All tests pass in CI/CD
- ✅ Performance tests within acceptable thresholds
- ✅ Security tests validate all input paths

### Developer Experience
- ✅ Tests run quickly (< 30 seconds for unit tests)
- ✅ Clear test failure messages
- ✅ Easy to write new tests
- ✅ Mock data readily available
- ✅ Documentation for test patterns

## Timeline & Approval Request

**Total Estimated Time**: 12-15 hours
**Priority**: Critical (blocks all other development)

**Questions for Approval**:
1. Should I proceed with this comprehensive testing plan?
2. Any specific test scenarios you want prioritized?
3. Do you want me to set up the testing infrastructure first, or implement tests alongside the existing code?
4. Any preferred testing tools or patterns I should use/avoid?

**Next Steps After Approval**:
1. Set up testing infrastructure and CI/CD
2. Implement backend API tests
3. Create frontend component tests  
4. Add MCP server and search tests
5. Implement E2E tests for critical flows
6. Generate coverage reports and documentation

This testing strategy ensures robust foundation for all teams while maintaining development velocity.