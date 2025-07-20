/**
 * Shared TypeScript types for COGENT
 * These types match the OpenAPI specification and SQLAlchemy models
 */

// User types
export interface User {
  id: string;
  email: string;
  name?: string | null;
  githubId?: string | null;
  googleId?: string | null;
  createdAt: string;
}

// Project types
export interface Project {
  id: string;
  name: string;
  userId: string;
  repoUrl?: string | null;
  apiKey: string;
  createdAt: string;
}

// Document types
export interface Document {
  id: string;
  projectId: string;
  filePath: string;
  content: string;
  summary: string;
  createdAt: string;
  updatedAt: string;
}

// Search types
export interface SearchResult {
  documentId: string;
  filePath: string;
  content: string;
  relevanceScore: number;
}

// Request types
export interface LoginRequest {
  provider: 'github' | 'google';
  code: string;
}

export interface LoginResponse {
  user: User;
  expiresAt: string;
}

export interface RefreshResponse {
  expiresAt: string;
}

export interface CreateProjectRequest {
  name: string;
  repoUrl?: string | null;
}

export interface UpdateProjectRequest {
  name?: string;
  repoUrl?: string | null;
}

export interface CreateDocumentRequest {
  filePath: string;
  content: string;
  summary: string;
}

export interface UpdateUserRequest {
  name?: string | null;
}

export interface SearchRequest {
  query: string;
  limit?: number;
  offset?: number;
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
  limit: number;
  offset: number;
}

export interface SearchResponse {
  results: SearchResult[];
  total: number;
  query: string;
}

// Usage types
export interface UsageStats {
  totalTokens: number;
  totalCost: number;
  documentsGenerated: number;
  searchesPerformed: number;
  dailyUsage?: DailyUsage[];
}

export interface DailyUsage {
  date: string;
  tokens: number;
  cost: number;
}

// Error types
export interface ApiError {
  error: string;
  message: string;
  details?: Record<string, any>;
}

// Auth types
export type AuthProvider = 'github' | 'google';

// API configuration
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

// Helper type guards
export function isApiError(error: any): error is ApiError {
  return error && typeof error.error === 'string' && typeof error.message === 'string';
}

export function isUser(obj: any): obj is User {
  return obj && typeof obj.id === 'string' && typeof obj.email === 'string';
}

export function isProject(obj: any): obj is Project {
  return obj && typeof obj.id === 'string' && typeof obj.name === 'string' && typeof obj.apiKey === 'string';
}