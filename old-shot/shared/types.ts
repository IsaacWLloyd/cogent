/**
 * Shared TypeScript types for COGENT
 * These types match the OpenAPI specification and SQLAlchemy models
 * Updated to match SPRINT0_SPEC.md Extended Schema
 */

// Enums
export type VisibilityType = 'private' | 'public';
export type OperationType = 'search' | 'generate' | 'mcp_call';
export type SearchType = 'full_text' | 'semantic' | 'hybrid';

// Core entity types
export interface User {
  id: string;
  clerk_id: string;
  email: string;
  name: string;
  created_at: string;
  updated_at: string;
  settings_json?: Record<string, any> | null;
  clerk_org_id?: string | null;
  last_seen?: string | null;
}

export interface Project {
  id: string;
  name: string;
  user_id: string;
  github_repo_url: string;
  created_at: string;
  updated_at: string;
  description?: string | null;
  visibility: VisibilityType;
  settings_json?: Record<string, any> | null;
  branch_name: string;
  include_patterns: string[];
  exclude_patterns: string[];
}

export interface Document {
  id: string;
  project_id: string;
  file_path: string;
  content: string;
  summary: string;
  commit_hash: string;
  created_at: string;
  updated_at: string;
  version: number;
  language?: string | null;
  imports?: string[] | null;
  exports?: string[] | null;
  references?: string[] | null;
}

export interface ApiKey {
  id: string;
  project_id: string;
  name: string;
  created_at: string;
  last_used?: string | null;
  // key_hash is not exposed in API responses
}

export interface Usage {
  id: string;
  project_id: string;
  timestamp: string;
  operation_type: OperationType;
  tokens_used: number;
  cost: number;
  llm_model: string;
  endpoint_called: string;
  response_time?: number | null;
}

// Clerk integration types
export interface ClerkUser {
  id: string;
  email_addresses: Array<{
    email_address: string;
    id: string;
  }>;
  first_name?: string | null;
  last_name?: string | null;
  created_at: number;
  updated_at: number;
}

export interface ClerkWebhook {
  type: 'user.created' | 'user.updated' | 'user.deleted';
  data: ClerkUser;
}

// Request types
export interface CreateProjectRequest {
  name: string;
  github_repo_url: string;
  description?: string;
  visibility?: VisibilityType;
  branch_name?: string;
  include_patterns?: string[];
  exclude_patterns?: string[];
}

export interface UpdateProjectRequest {
  name?: string;
  description?: string;
  visibility?: VisibilityType;
  settings_json?: Record<string, any>;
  branch_name?: string;
  include_patterns?: string[];
  exclude_patterns?: string[];
}

export interface CreateDocumentRequest {
  file_path: string;
  content: string;
  summary: string;
  commit_hash: string;
  language?: string;
  imports?: string[];
  exports?: string[];
  references?: string[];
}

export interface SearchRequest {
  query: string;
  search_type?: SearchType;
  max_results?: number;
  filters?: {
    language?: string;
    file_patterns?: string[];
    date_range?: {
      start: string;
      end: string;
    };
  };
}

export interface CreateApiKeyRequest {
  name: string;
}

export interface UpdateUserRequest {
  name?: string;
  settings_json?: Record<string, any>;
}

// Response types
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

export interface ProjectsResponse {
  projects: Project[];
  total: number;
  limit: number;
  offset: number;
}

export interface DocumentsResponse {
  documents: Document[];
  total: number;
}

export interface SearchResult {
  document: Document;
  score: number;
  highlights: string[];
}

export interface SearchResponse {
  results: SearchResult[];
  total_results: number;
  search_time_ms: number;
}

export interface ApiKeyResponse {
  api_keys: ApiKey[];
}

export interface ApiKeyCreateResponse {
  api_key: ApiKey;
  key: string; // Only returned once upon creation
}

export interface UsageStatsResponse {
  total_operations: number;
  total_tokens: number;
  total_cost: number;
  operations_by_type: {
    search?: number;
    generate?: number;
    mcp_call?: number;
  };
  daily_usage: Array<{
    date: string;
    operations: number;
    tokens: number;
    cost: number;
  }>;
}

// GitHub integration types
export interface GitHubRepository {
  id: number;
  name: string;
  full_name: string;
  private: boolean;
  html_url: string;
  description?: string | null;
  default_branch: string;
  permissions: {
    admin: boolean;
    push: boolean;
    pull: boolean;
  };
}

export interface GitHubFile {
  name: string;
  path: string;
  sha: string;
  size: number;
  type: 'file' | 'dir';
  content?: string | null;
  encoding?: string | null;
}

export interface GitHubFileUpdate {
  path: string;
  content: string;
  message: string;
  branch?: string;
  sha?: string | null;
}

export interface GitHubReposResponse {
  repositories: GitHubRepository[];
}

export interface GitHubFilesResponse {
  files: GitHubFile[];
}

// Error types
export interface ApiError {
  error: string;
  message: string;
  details?: Record<string, any>;
}

// MCP Server types
export interface DocumentContext {
  project_id: string;
  file_path: string;
  content: string;
  summary: string;
  relevance_score?: number;
}

export interface ContextRequest {
  project_id: string;
  query: string;
  max_results?: number;
}

export interface ContextResponse {
  contexts: DocumentContext[];
  total_found: number;
}

// Utility types
export type AuthProvider = 'github' | 'google' | 'email';

// API configuration
export const API_BASE_URL = typeof window !== 'undefined' 
  ? (window as any).__RUNTIME_CONFIG__?.API_BASE_URL || '/api'
  : process.env.NEXT_PUBLIC_API_BASE_URL || '/api';

// Type guards
export function isApiError(error: any): error is ApiError {
  return error && typeof error.error === 'string' && typeof error.message === 'string';
}

export function isUser(obj: any): obj is User {
  return obj && 
    typeof obj.id === 'string' && 
    typeof obj.clerk_id === 'string' &&
    typeof obj.email === 'string' &&
    typeof obj.name === 'string';
}

export function isProject(obj: any): obj is Project {
  return obj && 
    typeof obj.id === 'string' && 
    typeof obj.name === 'string' && 
    typeof obj.user_id === 'string' &&
    typeof obj.github_repo_url === 'string';
}

export function isDocument(obj: any): obj is Document {
  return obj && 
    typeof obj.id === 'string' && 
    typeof obj.project_id === 'string' &&
    typeof obj.file_path === 'string' &&
    typeof obj.content === 'string' &&
    typeof obj.summary === 'string' &&
    typeof obj.commit_hash === 'string';
}

export function isVisibilityType(value: any): value is VisibilityType {
  return value === 'private' || value === 'public';
}

export function isOperationType(value: any): value is OperationType {
  return value === 'search' || value === 'generate' || value === 'mcp_call';
}

export function isSearchType(value: any): value is SearchType {
  return value === 'full_text' || value === 'semantic' || value === 'hybrid';
}

// Helper functions for data validation
export function validateCreateProjectRequest(data: any): data is CreateProjectRequest {
  return data &&
    typeof data.name === 'string' &&
    typeof data.github_repo_url === 'string' &&
    data.name.length > 0 &&
    data.github_repo_url.length > 0;
}

export function validateSearchRequest(data: any): data is SearchRequest {
  return data &&
    typeof data.query === 'string' &&
    data.query.length > 0 &&
    (data.max_results === undefined || (typeof data.max_results === 'number' && data.max_results > 0));
}

// Constants
export const DEFAULT_PAGE_SIZE = 20;
export const MAX_PAGE_SIZE = 100;
export const DEFAULT_SEARCH_RESULTS = 10;
export const MAX_SEARCH_RESULTS = 50;

export const DEFAULT_INCLUDE_PATTERNS = ['**/*'];
export const DEFAULT_EXCLUDE_PATTERNS = ['node_modules/**', '.git/**', '.next/**', 'dist/**', 'build/**'];

// File extension to language mapping
export const LANGUAGE_MAP: Record<string, string> = {
  '.js': 'javascript',
  '.jsx': 'javascript',
  '.ts': 'typescript',
  '.tsx': 'typescript',
  '.py': 'python',
  '.java': 'java',
  '.go': 'go',
  '.rs': 'rust',
  '.cpp': 'cpp',
  '.c': 'c',
  '.cs': 'csharp',
  '.php': 'php',
  '.rb': 'ruby',
  '.swift': 'swift',
  '.kt': 'kotlin',
  '.scala': 'scala',
  '.sh': 'bash',
  '.sql': 'sql',
  '.json': 'json',
  '.yaml': 'yaml',
  '.yml': 'yaml',
  '.md': 'markdown',
  '.html': 'html',
  '.css': 'css',
  '.scss': 'scss',
  '.sass': 'sass',
  '.vue': 'vue',
  '.svelte': 'svelte',
};

export function getLanguageFromPath(filePath: string): string | null {
  const ext = filePath.toLowerCase().substring(filePath.lastIndexOf('.'));
  return LANGUAGE_MAP[ext] || null;
}

// Export all types for convenience
export * from './database' // Re-export Python types if needed