import { useParams } from 'react-router-dom'
import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { Separator } from '@/components/ui/separator'
import { useProject, useDocuments } from '@/hooks/useApi'
import { Search, FileText, Calendar, Eye } from 'lucide-react'

export function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [searchQuery, setSearchQuery] = useState('')
  
  const { data: project, isLoading: projectLoading } = useProject(id!)
  const { data: documentsData, isLoading: documentsLoading } = useDocuments(id!)

  if (projectLoading) {
    return <ProjectDetailSkeleton />
  }

  if (!project) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold">Project Not Found</h1>
        <p className="text-muted-foreground mt-2">
          The project you're looking for doesn't exist or you don't have access to it.
        </p>
      </div>
    )
  }

  const documents = documentsData?.documents || []
  const filteredDocuments = documents.filter(doc =>
    doc.filePath.toLowerCase().includes(searchQuery.toLowerCase()) ||
    doc.summary.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">{project.name}</h1>
        <p className="text-muted-foreground">
          Browse and search your project documentation
        </p>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search documents..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10"
        />
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Documents</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {documentsLoading ? '...' : documents.length}
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Last Updated</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {documents.length > 0 
                ? new Date(Math.max(...documents.map(d => new Date(d.updatedAt).getTime()))).toLocaleDateString()
                : 'Never'
              }
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Coverage</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {documentsLoading ? '...' : `${Math.min(100, documents.length * 10)}%`}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Documents List */}
      <Card>
        <CardHeader>
          <CardTitle>Documentation Files</CardTitle>
          <CardDescription>
            {searchQuery 
              ? `Found ${filteredDocuments.length} documents matching "${searchQuery}"`
              : `${documents.length} total documents`
            }
          </CardDescription>
        </CardHeader>
        <CardContent>
          {documentsLoading ? (
            <DocumentListSkeleton />
          ) : filteredDocuments.length === 0 ? (
            <div className="text-center py-8">
              <FileText className="mx-auto h-12 w-12 text-muted-foreground" />
              <h3 className="mt-2 text-sm font-semibold">No documents found</h3>
              <p className="mt-1 text-sm text-muted-foreground">
                {searchQuery 
                  ? 'Try adjusting your search query'
                  : 'Start coding to generate documentation automatically'
                }
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredDocuments.map((document, index) => (
                <div key={document.id}>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h4 className="font-medium">{document.filePath}</h4>
                      <p className="text-sm text-muted-foreground mt-1">
                        {document.summary}
                      </p>
                      <p className="text-xs text-muted-foreground mt-2">
                        Updated {new Date(document.updatedAt).toLocaleDateString()}
                      </p>
                    </div>
                    <Button variant="outline" size="sm">
                      View
                    </Button>
                  </div>
                  {index < filteredDocuments.length - 1 && <Separator className="mt-4" />}
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

function ProjectDetailSkeleton() {
  return (
    <div className="space-y-6">
      <div>
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-4 w-96 mt-2" />
      </div>
      <Skeleton className="h-10 w-full" />
      <div className="grid gap-4 md:grid-cols-3">
        {Array.from({ length: 3 }).map((_, i) => (
          <Card key={i}>
            <CardHeader>
              <Skeleton className="h-4 w-32" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-8 w-16" />
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

function DocumentListSkeleton() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 5 }).map((_, i) => (
        <div key={i} className="space-y-2">
          <Skeleton className="h-5 w-64" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-3 w-32" />
        </div>
      ))}
    </div>
  )
}