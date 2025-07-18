package shared

// MCP (Model Context Protocol) related types and constants

// MCPToolName represents the tools available in the MCP server
type MCPToolName string

const (
	MCPToolSearchDocs    MCPToolName = "search_documentation"
	MCPToolGetContext    MCPToolName = "get_context"
	MCPToolValidateRelevance MCPToolName = "validate_relevance"
)

// MCPToolDefinition represents a tool definition for the MCP protocol
type MCPToolDefinition struct {
	Name        MCPToolName            `json:"name"`
	Description string                 `json:"description"`
	InputSchema map[string]interface{} `json:"inputSchema"`
}

// MCPToolRequest represents a tool execution request
type MCPToolRequest struct {
	Tool      MCPToolName            `json:"tool"`
	Arguments map[string]interface{} `json:"arguments"`
}

// MCPToolResponse represents a tool execution response
type MCPToolResponse struct {
	Success bool        `json:"success"`
	Content interface{} `json:"content,omitempty"`
	Error   string      `json:"error,omitempty"`
}

// ContextRequest represents a request for context injection
type ContextRequest struct {
	ProjectID     string   `json:"project_id"`
	CurrentFile   string   `json:"current_file,omitempty"`
	Query         string   `json:"query"`
	MaxTokens     int      `json:"max_tokens,omitempty"`
	FileTypes     []string `json:"file_types,omitempty"`
	IncludePaths  []string `json:"include_paths,omitempty"`
	ExcludePaths  []string `json:"exclude_paths,omitempty"`
}

// ContextResponse represents the context provided to Claude Code
type ContextResponse struct {
	Context   string           `json:"context"`
	Sources   []ContextSource  `json:"sources"`
	TokenUsed int              `json:"tokens_used"`
}

// ContextSource represents a source of context information
type ContextSource struct {
	FilePath    string  `json:"file_path"`
	LineRange   string  `json:"line_range,omitempty"`
	Relevance   float64 `json:"relevance"`
	Summary     string  `json:"summary"`
}

// RelevanceValidationRequest represents a request to validate search result relevance
type RelevanceValidationRequest struct {
	Query   string         `json:"query"`
	Results []SearchResult `json:"results"`
}

// RelevanceValidationResponse represents the validation response
type RelevanceValidationResponse struct {
	FilteredResults []SearchResult `json:"filtered_results"`
	Reasoning       string         `json:"reasoning"`
}