package shared

import (
	"time"
)

// Project represents a code project that COGENT is managing
type Project struct {
	ID              string            `json:"id" db:"id"`
	Name            string            `json:"name" db:"name"`
	Path            string            `json:"path" db:"path"`
	UserID          string            `json:"user_id" db:"user_id"`
	APIKey          string            `json:"api_key" db:"api_key"`
	Config          ProjectConfig     `json:"config" db:"config"`
	CreatedAt       time.Time         `json:"created_at" db:"created_at"`
	UpdatedAt       time.Time         `json:"updated_at" db:"updated_at"`
}

// ProjectConfig holds project-specific settings
type ProjectConfig struct {
	IncludePatterns    []string                `json:"include_patterns"`
	ExcludePatterns    []string                `json:"exclude_patterns"`
	DocumentationStyle DocumentationStyle      `json:"documentation_style"`
	Visibility         ProjectVisibility       `json:"visibility"`
	Templates          map[string]string       `json:"templates"`
}

// DocumentationStyle defines the format and detail level for generated docs
type DocumentationStyle struct {
	Format      string `json:"format"`      // "markdown", "restructured_text"
	DetailLevel string `json:"detail_level"` // "brief", "detailed", "comprehensive"
	Language    string `json:"language"`    // "javascript", "python", "go", etc.
}

// ProjectVisibility controls who can access the project documentation
type ProjectVisibility string

const (
	VisibilityPrivate ProjectVisibility = "private"
	VisibilityPublic  ProjectVisibility = "public"
)

// User represents a user of the COGENT system
type User struct {
	ID        string    `json:"id" db:"id"`
	Email     string    `json:"email" db:"email"`
	Name      string    `json:"name" db:"name"`
	Provider  string    `json:"provider" db:"provider"` // "github", "google"
	ExternalID string   `json:"external_id" db:"external_id"`
	CreatedAt time.Time `json:"created_at" db:"created_at"`
	UpdatedAt time.Time `json:"updated_at" db:"updated_at"`
}

// Documentation represents a generated documentation file
type Documentation struct {
	ID        string    `json:"id" db:"id"`
	ProjectID string    `json:"project_id" db:"project_id"`
	FilePath  string    `json:"file_path" db:"file_path"`
	Content   string    `json:"content" db:"content"`
	Hash      string    `json:"hash" db:"hash"` // Hash of source file for change detection
	CreatedAt time.Time `json:"created_at" db:"created_at"`
	UpdatedAt time.Time `json:"updated_at" db:"updated_at"`
}

// HookEvent represents an event that triggers documentation generation
type HookEvent struct {
	Type      HookEventType `json:"type"`
	Timestamp time.Time     `json:"timestamp"`
	Tool      string        `json:"tool"`
	FilePath  string        `json:"file_path"`
	Content   string        `json:"content,omitempty"`
	Changes   []FileChange  `json:"changes,omitempty"`
}

// HookEventType defines the types of hook events
type HookEventType string

const (
	EventTypePostToolUse HookEventType = "post_tool_use"
	EventTypePreCommit   HookEventType = "pre_commit"
)

// FileChange represents a change to a file
type FileChange struct {
	Operation string `json:"operation"` // "create", "update", "delete"
	Path      string `json:"path"`
	OldHash   string `json:"old_hash,omitempty"`
	NewHash   string `json:"new_hash,omitempty"`
}

// MCPSearchRequest represents a search request from the MCP server
type MCPSearchRequest struct {
	ProjectID string   `json:"project_id"`
	Query     string   `json:"query"`
	FileTypes []string `json:"file_types,omitempty"`
	MaxResults int     `json:"max_results,omitempty"`
}

// MCPSearchResponse represents search results returned to the MCP server
type MCPSearchResponse struct {
	Results []SearchResult `json:"results"`
	Total   int           `json:"total"`
}

// SearchResult represents a single search result
type SearchResult struct {
	FilePath    string  `json:"file_path"`
	Content     string  `json:"content"`
	Relevance   float64 `json:"relevance"`
	LineNumbers []int   `json:"line_numbers,omitempty"`
	Summary     string  `json:"summary,omitempty"`
}

// APIResponse is a standard response wrapper for API endpoints
type APIResponse[T any] struct {
	Success bool   `json:"success"`
	Data    T      `json:"data,omitempty"`
	Error   string `json:"error,omitempty"`
}

// Usage represents billing usage for a project
type Usage struct {
	ID           string    `json:"id" db:"id"`
	ProjectID    string    `json:"project_id" db:"project_id"`
	UserID       string    `json:"user_id" db:"user_id"`
	LLMProvider  string    `json:"llm_provider" db:"llm_provider"`
	Model        string    `json:"model" db:"model"`
	InputTokens  int       `json:"input_tokens" db:"input_tokens"`
	OutputTokens int       `json:"output_tokens" db:"output_tokens"`
	Cost         float64   `json:"cost" db:"cost"`
	Timestamp    time.Time `json:"timestamp" db:"timestamp"`
}