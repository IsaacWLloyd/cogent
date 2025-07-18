# COGENT Development Roadmap - One Week Sprint

## Overview
This roadmap is optimized for 3-5 parallel development tracks to deliver the MVP: Claude Code hooks + MCP server for documentation generation and context injection, with full web dashboard and payment integration.

## Parallel Development Tracks

### 🔧 Track 1: Core Hook System (Days 1-7)
**Agent Focus: Core Infrastructure**

**Phase 1: Hook Foundation**
- Set up Go project structure with `/backend`, `/hooks`, `/shared` directories
- Implement PostToolUse hook detection for Edit/Write/MultiEdit tools
- Create file change detection and diff analysis
- Build synchronous documentation prompt system
- Implement subagent spawning via Task tool for async completion

**Phase 2: Documentation Generation**
- Design JS/TS documentation templates (file purpose, functions, dependencies, connections)
- Build AST parsing for JavaScript/TypeScript files
- Implement incremental documentation updates
- Create cross-reference tracking between files
- Add error handling with placeholder docs on failures

**Phase 3: Hook Integration**
- Build Claude Code settings integration (`hooks.json` configuration)
- Implement timeout handling (30s sync, unlimited async)
- Create warning system for documentation failures
- Test hook reliability and error recovery

### 🌐 Track 2: MCP Server (Days 1-7)
**Agent Focus: Context System**

**Phase 1: MCP Infrastructure**
- Set up MCP server project structure
- Implement Model Context Protocol communication
- Build API integration with backend for documentation search
- Create project-scoped API key authentication

**Phase 2: Search & Retrieval**
- Implement hybrid search (full-text + semantic)
- Build PostgreSQL full-text search queries
- Integrate vector embeddings for semantic matching
- Create relevance validation using LLM calls

**Phase 3: Context Injection**
- Build context formatting for Claude Code consumption
- Implement smart context windowing (prioritize relevance)
- Add real-time documentation updates via WebSocket
- Create fallback mechanisms for search failures

### 🗄️ Track 3: Backend API (Days 1-6)
**Agent Focus: Data Layer**

**Phase 1: Database & Auth**
- Set up PostgreSQL with projects, users, documentation tables
- Implement OAuth 2.0 with GitHub + Google providers
- Build JWT token management and API key generation
- Create user registration and project onboarding flow

**Phase 2: Core APIs**
- Build project CRUD operations
- Implement documentation storage and retrieval APIs
- Create search endpoints (full-text + vector)
- Add user management and project permissions

**Phase 3: Advanced Features**
- Build WebSocket server for real-time updates
- Implement rate limiting per project
- Add usage metering for OpenRouter API calls
- Create analytics and monitoring endpoints

### 🎨 Track 4: Frontend Dashboard (Days 2-7)
**Agent Focus: User Interface**

**Phase 1: Foundation**
- Set up React + Vite + SHADCN project
- Implement OAuth login flow (GitHub + Google)
- Build responsive dashboard layout
- Create project selection and overview interface

**Phase 2: Core Features**
- Build documentation search interface with filters
- Implement project management (create, configure, delete)
- Add file pattern inclusion/exclusion settings
- Create documentation visibility controls (public/private)

**Phase 3: Advanced UI**
- Build usage analytics dashboard with charts
- Implement real-time documentation updates
- Add documentation template customization
- Create billing and payment interface integration

### 💳 Track 5: Payment Integration (Days 4-7)
**Agent Focus: Monetization**

**Phase 1: Polar Setup**
- Integrate Polar payment processing
- Build subscription plans (usage-based pricing)
- Implement webhook handlers for payment events
- Create billing history and invoice management

**Phase 2: Usage Tracking**
- Build OpenRouter API usage metering
- Implement project-level usage limits
- Create billing calculations (usage + margin)
- Add payment status checks and enforcement

**Phase 3: Business Logic**
- Build trial period management
- Implement usage overage handling
- Create payment failure recovery flows
- Add billing notifications and alerts

## Critical Dependencies & Sequencing

### Dependency Chain
1. **Database Schema** → All other tracks depend on this
2. **OAuth System** → Frontend and API protection
3. **Basic Hook** → MCP server context needs
4. **Core APIs** → Frontend data requirements
5. **Documentation Generation** → Search functionality

### Parallel Work Optimization
- **Track 1 & 2** can work independently after shared types are defined
- **Track 3** must complete auth before Track 4 login
- **Track 4** can mock APIs initially, integrate later
- **Track 5** can start once user/project models exist

## Week Structure

### Setup & Foundation
- Initialize all 5 project directories with basic structure
- Define shared types and interfaces in `/shared`
- Set up development environments and databases
- Create initial documentation templates

### Core Development
- Tracks 1-3 work on MVP functionality
- Track 4 builds UI mockups and static interfaces
- Track 5 researches Polar integration requirements

### Integration Phase
- Connect MCP server to backend APIs
- Integrate frontend with real backend data
- Test end-to-end hook → documentation → search flow
- Add payment processing to user flows

### Testing & Polish
- End-to-end testing of complete user journey
- Performance optimization for search and documentation
- Error handling and edge case coverage
- Documentation and deployment preparation

## Key Deliverables

### MVP Core (Required for Launch)
- ✅ Claude Code hook that forces documentation writing
- ✅ MCP server that provides relevant context
- ✅ Web dashboard for project management
- ✅ OAuth authentication system
- ✅ Basic documentation search functionality

### Business Requirements
- ✅ Polar payment integration
- ✅ Usage-based pricing model
- ✅ Project-level API key system
- ✅ Rate limiting and usage tracking

### User Experience
- ✅ One-command installation script
- ✅ Seamless OAuth onboarding
- ✅ Real-time documentation updates
- ✅ Intuitive search and discovery

## Risk Mitigation

### Technical Risks
- **Hook Reliability**: Extensive testing with various file types and edge cases
- **Search Performance**: Database indexing and query optimization
- **Real-time Updates**: WebSocket fallback mechanisms

### Integration Risks
- **Claude Code Compatibility**: Test with multiple Claude Code versions
- **OAuth Provider Changes**: Abstract auth layer for easy provider swapping
- **Payment Processing**: Polar integration testing in sandbox mode

### Timeline Risks
- **Parallel Development**: Daily standup to sync shared interfaces
- **Dependency Blocking**: Mock interfaces to enable parallel work
- **Scope Creep**: Strict MVP focus, defer nice-to-have features

## Success Metrics

### Technical Success
- Hook triggers correctly on 100% of file modifications
- Search returns relevant results in <500ms
- Documentation generation completes in <30s
- Zero data loss during async processing

### Business Success
- Complete user onboarding flow in <5 minutes
- Successful payment processing integration
- Project setup and first documentation in <10 minutes
- Billing and usage tracking accuracy

### User Experience Success
- Intuitive dashboard navigation
- Clear documentation quality improvements
- Seamless Claude Code integration
- Reliable context provision to Claude Code

This roadmap optimizes for parallel development while ensuring critical dependencies are met. Each track can work independently with well-defined interfaces, enabling maximum development velocity within the one-week timeline.
