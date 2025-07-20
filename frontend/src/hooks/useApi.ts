import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { mockUser, mockProjects, mockDocuments, mockSearchResults, mockUsageStats } from '@/lib/mock-data'
import type { 
  User,
  Project,
  Document,
  CreateProjectRequest,
  UpdateProjectRequest,
  CreateDocumentRequest,
  UpdateUserRequest,
  SearchRequest,
  SearchResponse,
  ProjectsResponse,
  DocumentsResponse,
  UsageStats
} from '@shared/types'

// Environment flag to enable/disable mocking
const USE_MOCK_DATA = import.meta.env.DEV

// Query Keys
export const queryKeys = {
  user: ['user'] as const,
  projects: ['projects'] as const,
  project: (id: string) => ['project', id] as const,
  documents: (projectId: string) => ['documents', projectId] as const,
  usage: ['usage'] as const,
  search: (projectId: string, query: string) => ['search', projectId, query] as const,
}

// User hooks
export function useUser() {
  return useQuery({
    queryKey: queryKeys.user,
    queryFn: USE_MOCK_DATA 
      ? () => Promise.resolve(mockUser)
      : () => api.getProfile(),
  })
}

export function useUpdateUser() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: USE_MOCK_DATA
      ? (data: UpdateUserRequest) => Promise.resolve({ ...mockUser, ...data })
      : (data: UpdateUserRequest) => api.updateProfile(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.user })
    },
  })
}

export function useUsage() {
  return useQuery({
    queryKey: queryKeys.usage,
    queryFn: USE_MOCK_DATA
      ? () => Promise.resolve(mockUsageStats)
      : () => api.getUsage(),
  })
}

// Project hooks
export function useProjects() {
  return useQuery({
    queryKey: queryKeys.projects,
    queryFn: USE_MOCK_DATA
      ? (): Promise<ProjectsResponse> => Promise.resolve({
          projects: mockProjects,
          total: mockProjects.length,
          limit: 20,
          offset: 0,
        })
      : () => api.getProjects(),
  })
}

export function useProject(id: string) {
  return useQuery({
    queryKey: queryKeys.project(id),
    queryFn: USE_MOCK_DATA
      ? () => Promise.resolve(mockProjects.find(p => p.id === id) || mockProjects[0])
      : () => api.getProject(id),
    enabled: !!id,
  })
}

export function useCreateProject() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: USE_MOCK_DATA
      ? (data: CreateProjectRequest): Promise<Project> => {
          const newProject: Project = {
            id: `project-${Date.now()}`,
            name: data.name,
            userId: mockUser.id,
            repoUrl: data.repoUrl || null,
            apiKey: `pk_live_${Math.random().toString(36).substring(7)}`,
            createdAt: new Date().toISOString(),
          }
          return Promise.resolve(newProject)
        }
      : (data: CreateProjectRequest) => api.createProject(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.projects })
    },
  })
}

export function useUpdateProject() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: USE_MOCK_DATA
      ? ({ id, data }: { id: string; data: UpdateProjectRequest }) => {
          const project = mockProjects.find(p => p.id === id) || mockProjects[0]
          return Promise.resolve({ ...project, ...data })
        }
      : ({ id, data }: { id: string; data: UpdateProjectRequest }) => api.updateProject(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.projects })
      queryClient.invalidateQueries({ queryKey: queryKeys.project(id) })
    },
  })
}

export function useDeleteProject() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: USE_MOCK_DATA
      ? (id: string) => Promise.resolve()
      : (id: string) => api.deleteProject(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.projects })
    },
  })
}

// Document hooks
export function useDocuments(projectId: string) {
  return useQuery({
    queryKey: queryKeys.documents(projectId),
    queryFn: USE_MOCK_DATA
      ? (): Promise<DocumentsResponse> => {
          const projectDocs = mockDocuments.filter(d => d.projectId === projectId)
          return Promise.resolve({
            documents: projectDocs,
            total: projectDocs.length,
            limit: 50,
            offset: 0,
          })
        }
      : () => api.getDocuments(projectId),
    enabled: !!projectId,
  })
}

export function useCreateDocument() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: USE_MOCK_DATA
      ? ({ projectId, data }: { projectId: string; data: CreateDocumentRequest }): Promise<Document> => {
          const newDoc: Document = {
            id: `doc-${Date.now()}`,
            projectId,
            filePath: data.filePath,
            content: data.content,
            summary: data.summary,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          }
          return Promise.resolve(newDoc)
        }
      : ({ projectId, data }: { projectId: string; data: CreateDocumentRequest }) => 
          api.createDocument(projectId, data),
    onSuccess: (_, { projectId }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.documents(projectId) })
    },
  })
}

// Search hooks
export function useSearchDocuments(projectId: string, query: string) {
  return useQuery({
    queryKey: queryKeys.search(projectId, query),
    queryFn: USE_MOCK_DATA
      ? (): Promise<SearchResponse> => Promise.resolve({
          results: mockSearchResults,
          total: mockSearchResults.length,
          query,
        })
      : () => api.searchDocuments(projectId, { query }),
    enabled: !!projectId && !!query && query.length > 0,
  })
}