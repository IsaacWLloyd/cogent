# COGENT Frontend Dashboard

React + Vite web application providing user interface for project management, documentation browsing, and system configuration.

## Architecture

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite 6
- **Styling**: Tailwind CSS + Shadcn/ui
- **Routing**: React Router v6
- **State**: React Query + Context API
- **Auth**: OAuth 2.0 integration

## Key Features

- **Dashboard View**: Recent projects and activity
- **Project Management**: Create, configure, and browse projects
- **Documentation Search**: Full-text search with relevance ranking
- **Settings Interface**: Project configuration and API keys
- **Usage Analytics**: Billing and usage monitoring
- **OAuth Authentication**: GitHub and Google login

## Project Structure

- `/src/components` - Reusable UI components
- `/src/pages` - Page-level components
- `/src/hooks` - Custom React hooks
- `/src/lib` - Utility functions and API clients
- `/src/types` - TypeScript type definitions
- `/src/context` - React context providers

## Development

```bash
# Start with Docker
make dev

# Local development
npm install
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint
```

## Component Library

Uses Shadcn/ui components for consistent design system:
- Buttons, Forms, Modals
- Data Tables with sorting/filtering
- Navigation and Layout components
- Loading states and error boundaries

## API Integration

Frontend communicates with backend via REST API:
- Authentication tokens stored in localStorage
- Request interceptors for auth headers
- Error handling for API failures
- Loading states for async operations

## Track Assignments

This component is assigned to **Track 4: Frontend Dashboard Development**.