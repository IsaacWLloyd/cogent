# Sprint 1 Team 2: Frontend Foundation Implementation

## Project Context

You are working on **COGENT** (Code Organization and Generation Enhancement Tool), a comprehensive documentation system that forces Claude Code to generate and maintain documentation for every code file it creates or modifies.

**Sprint 0 has been completed** and established all foundational contracts:
- Complete OpenAPI specification (`openapi.yaml`) with all API endpoints defined
- SQLAlchemy database models (`backend/models.py`)
- Shared TypeScript and Python types (`shared/types.ts`, `shared/models.py`)
- Frontend package.json with React, TypeScript, Vite, and SHADCN UI dependencies
- Vite configuration with API proxy to backend

## Your Team's Responsibilities

As the **Frontend Foundation** team, you are responsible for implementing the React + TypeScript foundation that will serve as the web interface for COGENT. Your deliverables include:

### Core Infrastructure
- React application structure with TypeScript and Vite
- Routing structure using React Router for all major pages
- SHADCN UI component library setup with custom theme
- API client with mock responses for development
- State management setup (either Context API, Zustand, or other)
- Layout components (Dashboard shell, Sidebar, Header, Navigation)

### Pages & Components to Build

Based on the project requirements, you need to create these main pages:

**Authentication Pages**
- Login page with OAuth buttons (GitHub/Google)
- Logout confirmation
- Protected route wrapper

**Dashboard Pages**
- Main dashboard (shows most recent project)
- Project list view 
- Project detail view with documentation browser
- Settings pages (user profile, project settings)
- Usage analytics page (mock data)

**Core Layout Components**
- App shell with sidebar navigation
- Header with user menu and search
- Sidebar with project navigation
- Loading states and error boundaries
- Toast notifications for user feedback

### API Integration Layer
- HTTP client setup with proper error handling
- Mock API responses for all endpoints during development
- Request/response types using shared TypeScript definitions
- Authentication state management
- API key management for project settings

## Available Resources

You have access to these completed Sprint 0 deliverables:

1. **Shared Types** (`shared/types.ts`): Complete TypeScript interfaces for User, Project, Document, and API requests/responses
2. **OpenAPI Specification** (`openapi.yaml`): Detailed API contracts to build your HTTP client against
3. **Package Dependencies** (`frontend/package.json`): React, TypeScript, Vite, SHADCN UI, React Router, TanStack Query, Zustand already configured
4. **Vite Configuration** (`frontend/vite.config.ts`): Development server with API proxy to backend
5. **Mock Data** (`backend/mock_data.py`): Reference for realistic test data structure

## Technology Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite with Hot Module Replacement  
- **UI Library**: SHADCN UI (Tailwind CSS + Radix primitives)
- **Routing**: React Router v6
- **State Management**: TBD (Context API, Zustand, or other - you decide)
- **Data Fetching**: TanStack Query for async state management
- **Styling**: Tailwind CSS with custom theme
- **Icons**: Lucide React
- **Testing**: Vitest for unit tests

## Knowledge Gaps & Questions

Before writing your detailed implementation specification, I need you to research the existing codebase and ask me specific questions about these areas where you need clarification:

### 1. Application Architecture
- What should be our overall component organization strategy?
- How should we structure the src/ directory (components, pages, hooks, utils, etc.)?
- Should we use feature-based or type-based folder organization?
- What patterns should we follow for component composition and reusability?

### 2. State Management Strategy  
- Should we use React Context API, Zustand, or another state solution?
- How should we handle authentication state across the application?
- What's our strategy for caching API responses and optimistic updates?
- How should we manage form state and validation?

### 3. SHADCN UI Implementation
- What's our custom theme and color palette strategy?
- Which SHADCN components do we need to install and configure?
- How should we handle responsive design across different screen sizes?
- What's our approach to custom component variants and styling?

### 4. API Client Design
- Should we use TanStack Query, SWR, or plain fetch for API calls?
- How should we structure the mock API responses during development?
- What's our error handling strategy for network failures?
- How should we handle authentication headers and token refresh?

### 5. Routing & Navigation
- What should be our exact route structure and URL patterns?
- How should we handle protected routes and authentication guards?
- What's our strategy for loading states during route transitions?
- Should we implement nested routing for project-specific pages?

### 6. User Experience Design
- What should be the exact layout and navigation flow?
- How should we handle empty states (no projects, no documents)?
- What loading and error states do we need to design?
- What's our approach to search functionality in the UI?

### 7. Development Workflow
- What's our strategy for mocking API data during development?
- How should we handle environment variables and configuration?
- What testing strategy should we implement for components?
- How should we handle deployment and build optimization?

### 8. Integration Requirements
- How will the MCP server integration affect the frontend (if at all)?
- What project configuration UI do we need for the Claude Code hooks?
- How should we display documentation files and search results?
- What real-time features (if any) do we need to prepare for?

## Your Task

1. **Research Phase**: Examine the existing Sprint 0 deliverables, especially the shared types and OpenAPI specification
2. **Question Phase**: Ask me specific, focused questions about the knowledge gaps above, one area at a time  
3. **Specification Phase**: Once all gaps are filled, write a comprehensive implementation specification that includes:
   - Complete React application architecture
   - Detailed component hierarchy and page structures
   - SHADCN UI setup and theming approach
   - API client implementation with mock data strategy
   - State management solution with authentication handling
   - Routing configuration and protected route implementation
   - Testing approach with specific component test scenarios

## Directory Restrictions

**CRITICAL: You are STRICTLY LIMITED to working within these directories:**
- `/frontend/` - All React frontend code (src/, public/, components/, etc.)
- `/shared/` - Only for reading shared TypeScript types, NO modifications allowed

**FORBIDDEN DIRECTORIES:**
- `/backend/` - Assigned to Team 1
- `/mcp-server/` - Assigned to Team 3
- `/hooks/` - Will be handled separately
- Any other directories not explicitly listed above

**File Creation Rules:**
- Create new files ONLY within `/frontend/`
- Read existing files in `/shared/` for TypeScript types but DO NOT modify them
- If you need changes to shared types, ask for approval first
- Modify `/frontend/package.json`, `/frontend/vite.config.ts` as needed

## Git Commit Guidelines

**Commit Strategy - Logical, Atomic Commits:**
1. **One Feature Per Commit** - Each commit should represent one complete, working feature
2. **Commit Early and Often** - Don't wait until everything is done
3. **Meaningful Messages** - Use conventional commit format

**Required Commit Pattern:**
```
feat(frontend): add dashboard layout with sidebar navigation
feat(frontend): implement project list page with mock data
fix(frontend): resolve TypeScript type errors in API client
test(frontend): add unit tests for authentication components
style(frontend): setup SHADCN UI theme and component library
```

**Commit Frequency Guidelines:**
- After setting up basic React app structure and routing
- After implementing each major page/component (Dashboard, Project List, etc.)
- After setting up SHADCN UI and theming
- After implementing the API client with mock responses
- After adding state management solution
- After creating layout components (Header, Sidebar, etc.)
- After implementing each major feature (auth, search, settings)
- After writing tests for components

**Each commit must:**
- Pass TypeScript compilation with no errors
- Include relevant test coverage for new components
- Have working, renderable UI components
- Include clear commit message explaining the change
- Follow established code style and conventions

Remember: Your implementation must work seamlessly with the backend API defined in the OpenAPI specification. The frontend should be able to run independently with mocked API responses during parallel development.

**Start by asking me your first set of questions about the application architecture.**