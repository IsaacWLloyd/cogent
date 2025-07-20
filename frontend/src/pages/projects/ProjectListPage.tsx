import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'
import { Skeleton } from '@/components/ui/skeleton'
import { useProjects, useCreateProject } from '@/hooks/useApi'
import { Plus, Github, ExternalLink, Settings } from 'lucide-react'
import type { CreateProjectRequest } from '@shared/types'

export function ProjectListPage() {
  const navigate = useNavigate()
  const { data: projectsData, isLoading } = useProjects()
  const createProject = useCreateProject()
  
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [newProject, setNewProject] = useState<CreateProjectRequest>({
    name: '',
    repoUrl: '',
  })

  const handleCreateProject = async () => {
    if (!newProject.name.trim()) return
    
    try {
      const project = await createProject.mutateAsync({
        name: newProject.name.trim(),
        repoUrl: newProject.repoUrl.trim() || null,
      })
      
      setIsCreateDialogOpen(false)
      setNewProject({ name: '', repoUrl: '' })
      navigate(`/projects/${project.id}`)
    } catch (error) {
      console.error('Failed to create project:', error)
    }
  }

  if (isLoading) {
    return <ProjectListSkeleton />
  }

  const projects = projectsData?.projects || []

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Projects</h1>
          <p className="text-muted-foreground">
            Manage your code documentation projects
          </p>
        </div>
        
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              New Project
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create New Project</DialogTitle>
              <DialogDescription>
                Add a new project to start generating documentation
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <Label htmlFor="name">Project Name</Label>
                <Input
                  id="name"
                  value={newProject.name}
                  onChange={(e) => setNewProject(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="My Awesome Project"
                />
              </div>
              <div>
                <Label htmlFor="repoUrl">Repository URL (optional)</Label>
                <Input
                  id="repoUrl"
                  value={newProject.repoUrl}
                  onChange={(e) => setNewProject(prev => ({ ...prev, repoUrl: e.target.value }))}
                  placeholder="https://github.com/username/repo"
                />
              </div>
            </div>
            <DialogFooter>
              <Button 
                variant="outline" 
                onClick={() => setIsCreateDialogOpen(false)}
              >
                Cancel
              </Button>
              <Button 
                onClick={handleCreateProject}
                disabled={!newProject.name.trim() || createProject.isPending}
              >
                {createProject.isPending ? 'Creating...' : 'Create Project'}
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      {projects.length === 0 ? (
        <EmptyProjectList />
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {projects.map((project) => (
            <Card key={project.id} className="cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => navigate(`/projects/${project.id}`)}>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="truncate">{project.name}</span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation()
                      navigate(`/projects/${project.id}/settings`)
                    }}
                  >
                    <Settings className="h-4 w-4" />
                  </Button>
                </CardTitle>
                <CardDescription>
                  Created {new Date(project.createdAt).toLocaleDateString()}
                </CardDescription>
              </CardHeader>
              <CardContent>
                {project.repoUrl && (
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <Github className="h-4 w-4" />
                    <span className="truncate">{project.repoUrl}</span>
                    <ExternalLink className="h-3 w-3" />
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

function ProjectListSkeleton() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <Skeleton className="h-8 w-32" />
          <Skeleton className="h-4 w-64 mt-2" />
        </div>
        <Skeleton className="h-10 w-32" />
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <Card key={i}>
            <CardHeader>
              <Skeleton className="h-6 w-48" />
              <Skeleton className="h-4 w-32" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-4 w-64" />
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

function EmptyProjectList() {
  return (
    <Card className="text-center py-12">
      <CardHeader>
        <CardTitle>No Projects Yet</CardTitle>
        <CardDescription>
          Create your first project to start generating and managing documentation
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Dialog>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Create Your First Project
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create New Project</DialogTitle>
              <DialogDescription>
                Add a new project to start generating documentation
              </DialogDescription>
            </DialogHeader>
          </DialogContent>
        </Dialog>
      </CardContent>
    </Card>
  )
}