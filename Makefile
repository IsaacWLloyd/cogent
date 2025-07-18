# COGENT Development Makefile

.PHONY: help dev build test clean deps migrate seed

# Default target
help:
	@echo "COGENT Development Commands:"
	@echo "  make dev      - Start development environment"
	@echo "  make build    - Build all components"
	@echo "  make test     - Run all tests"
	@echo "  make clean    - Clean up containers and volumes"
	@echo "  make deps     - Install all dependencies"
	@echo "  make migrate  - Run database migrations"
	@echo "  make seed     - Seed database with test data"

# Start development environment
dev:
	@echo "Starting COGENT development environment..."
	docker-compose up --build

# Start development environment in background
dev-bg:
	@echo "Starting COGENT development environment in background..."
	docker-compose up --build -d

# Build all components
build:
	@echo "Building all components..."
	docker-compose build

# Run all tests
test:
	@echo "Running backend tests..."
	cd backend && go test ./...
	@echo "Running frontend tests..."
	cd frontend && npm test
	@echo "Running MCP server tests..."
	cd mcp-server && go test ./...

# Clean up development environment
clean:
	@echo "Cleaning up development environment..."
	docker-compose down -v --remove-orphans
	docker system prune -f

# Install dependencies
deps:
	@echo "Installing Go dependencies..."
	cd backend && go mod download
	cd mcp-server && go mod download
	cd shared && go mod download
	@echo "Installing Node.js dependencies..."
	cd frontend && npm install

# Run database migrations
migrate:
	@echo "Running database migrations..."
	docker-compose exec backend go run cmd/migrate/main.go

# Seed database with test data
seed:
	@echo "Seeding database with test data..."
	docker-compose exec backend go run cmd/seed/main.go

# Generate documentation
docs:
	@echo "Generating API documentation..."
	cd backend && swag init

# Lint all code
lint:
	@echo "Linting Go code..."
	cd backend && golangci-lint run
	cd mcp-server && golangci-lint run
	@echo "Linting frontend code..."
	cd frontend && npm run lint

# Format all code
fmt:
	@echo "Formatting Go code..."
	cd backend && go fmt ./...
	cd mcp-server && go fmt ./...
	cd shared && go fmt ./...
	@echo "Formatting frontend code..."
	cd frontend && npm run format

# Development logs
logs:
	docker-compose logs -f

# Stop development environment
stop:
	docker-compose stop

# Restart development environment
restart:
	docker-compose restart