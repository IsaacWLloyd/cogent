// TypeScript types that mirror the Go shared types

export interface Project {
  id: string;
  name: string;
  path: string;
  user_id: string;
  api_key: string;
  config: ProjectConfig;
  created_at: string;
  updated_at: string;
}

export interface ProjectConfig {
  include_patterns: string[];
  exclude_patterns: string[];
  documentation_style: DocumentationStyle;
  visibility: ProjectVisibility;
  templates: Record<string, string>;
}

export interface DocumentationStyle {
  format: string; // "markdown" | "restructured_text"
  detail_level: string; // "brief" | "detailed" | "comprehensive"
  language: string; // "javascript" | "python" | "go" etc.
}

export type ProjectVisibility = "private" | "public";

export interface User {
  id: string;
  email: string;
  name: string;
  provider: string; // "github" | "google"
  external_id: string;
  created_at: string;
  updated_at: string;
}

export interface Documentation {
  id: string;
  project_id: string;
  file_path: string;
  content: string;
  hash: string;
  created_at: string;
  updated_at: string;
}

export interface HookEvent {
  type: HookEventType;
  timestamp: string;
  tool: string;
  file_path: string;
  content?: string;
  changes?: FileChange[];
}

export type HookEventType = "post_tool_use" | "pre_commit";

export interface FileChange {
  operation: string; // "create" | "update" | "delete"
  path: string;
  old_hash?: string;
  new_hash?: string;
}

export interface MCPSearchRequest {
  project_id: string;
  query: string;
  file_types?: string[];
  max_results?: number;
}

export interface MCPSearchResponse {
  results: SearchResult[];
  total: number;
}

export interface SearchResult {
  file_path: string;
  content: string;
  relevance: number;
  line_numbers?: number[];
  summary?: string;
}

export interface APIResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface Usage {
  id: string;
  project_id: string;
  user_id: string;
  llm_provider: string;
  model: string;
  input_tokens: number;
  output_tokens: number;
  cost: number;
  timestamp: string;
}

// Dashboard-specific types
export interface DashboardStats {
  total_projects: number;
  total_docs: number;
  total_usage_cost: number;
  recent_activity: RecentActivity[];
}

export interface RecentActivity {
  type: "doc_generated" | "search_performed" | "project_created";
  project_name: string;
  timestamp: string;
  details: string;
}

// Auth types
export interface AuthUser {
  id: string;
  email: string;
  name: string;
  avatar_url?: string;
}

export interface LoginResponse {
  user: AuthUser;
  token: string;
  expires_at: string;
}