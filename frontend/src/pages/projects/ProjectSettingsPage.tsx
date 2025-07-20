import { useParams, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Skeleton } from '@/components/ui/skeleton'
import { useProject, useUpdateProject, useDeleteProject } from '@/hooks/useApi'
import { Copy, Trash2, Save, ExternalLink } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

export function ProjectSettingsPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { toast } = useToast()
  
  const { data: project, isLoading } = useProject(id!)
  const updateProject = useUpdateProject()
  const deleteProject = useDeleteProject()
  
  const [formData, setFormData] = useState({
    name: '',
    repoUrl: '',
  })
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)

  // Update form when project loads
  useEffect(() => {
    if (project) {
      setFormData({
        name: project.name,
        repoUrl: project.repoUrl || '',
      })
    }
  }, [project])

  const handleSave = async () => {
    if (!project || !formData.name.trim()) return
    
    try {
      await updateProject.mutateAsync({
        id: project.id,
        data: {
          name: formData.name.trim(),
          repoUrl: formData.repoUrl.trim() || null,
        }
      })
      
      toast({
        title: "Project updated",
        description: "Your project settings have been saved.",
      })
    } catch (error) {
      toast({
        title: "Update failed",
        description: "There was an error updating your project.",
        variant: "destructive",
      })
    }
  }

  const handleDelete = async () => {
    if (!project) return
    
    try {
      await deleteProject.mutateAsync(project.id)
      
      toast({
        title: "Project deleted",
        description: "Your project has been permanently deleted.",
      })
      
      navigate('/projects')
    } catch (error) {
      toast({
        title: "Delete failed",
        description: "There was an error deleting your project.",
        variant: "destructive",
      })
    }
  }

  const copyApiKey = () => {
    if (project?.apiKey) {
      navigator.clipboard.writeText(project.apiKey)
      toast({
        title: "API key copied",
        description: "The API key has been copied to your clipboard.",
      })
    }
  }

  if (isLoading) {
    return <ProjectSettingsSkeleton />
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

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Project Settings</h1>
        <p className="text-muted-foreground">
          Manage your project configuration and API access
        </p>
      </div>

      {/* Basic Settings */}
      <Card>
        <CardHeader>
          <CardTitle>Basic Information</CardTitle>
          <CardDescription>
            Update your project name and repository URL
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="name">Project Name</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
              placeholder="My Awesome Project"
            />
          </div>
          <div>
            <Label htmlFor="repoUrl">Repository URL</Label>
            <Input
              id="repoUrl"
              value={formData.repoUrl}
              onChange={(e) => setFormData(prev => ({ ...prev, repoUrl: e.target.value }))}
              placeholder="https://github.com/username/repo"
            />
            {project.repoUrl && (
              <div className="flex items-center gap-2 mt-2">
                <Button variant="outline" size="sm" asChild>
                  <a href={project.repoUrl} target="_blank" rel="noopener noreferrer">
                    <ExternalLink className="mr-2 h-4 w-4" />
                    Open Repository
                  </a>
                </Button>
              </div>
            )}
          </div>
          <Button 
            onClick={handleSave}
            disabled={updateProject.isPending || !formData.name.trim()}
          >
            <Save className="mr-2 h-4 w-4" />
            {updateProject.isPending ? 'Saving...' : 'Save Changes'}
          </Button>
        </CardContent>
      </Card>

      {/* API Key */}
      <Card>
        <CardHeader>
          <CardTitle>API Key</CardTitle>
          <CardDescription>
            Use this key to authenticate with the COGENT API and MCP server
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-2">
            <Textarea
              value={project.apiKey}
              readOnly
              className="font-mono text-sm resize-none"
              rows={2}
            />
            <Button variant="outline" onClick={copyApiKey}>
              <Copy className="h-4 w-4" />
            </Button>
          </div>
          <p className="text-sm text-muted-foreground mt-2">
            Keep this key secure. It provides full access to your project's documentation.
          </p>
        </CardContent>
      </Card>

      {/* Danger Zone */}
      <Card className="border-destructive">
        <CardHeader>
          <CardTitle className="text-destructive">Danger Zone</CardTitle>
          <CardDescription>
            Irreversible and destructive actions
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Dialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
            <DialogTrigger asChild>
              <Button variant="destructive">
                <Trash2 className="mr-2 h-4 w-4" />
                Delete Project
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Delete Project</DialogTitle>
                <DialogDescription>
                  Are you sure you want to delete "{project.name}"? This action cannot be undone.
                  All documentation and settings will be permanently lost.
                </DialogDescription>
              </DialogHeader>
              <DialogFooter>
                <Button 
                  variant="outline" 
                  onClick={() => setIsDeleteDialogOpen(false)}
                  disabled={deleteProject.isPending}
                >
                  Cancel
                </Button>
                <Button 
                  variant="destructive" 
                  onClick={handleDelete}
                  disabled={deleteProject.isPending}
                >
                  {deleteProject.isPending ? 'Deleting...' : 'Delete Project'}
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </CardContent>
      </Card>
    </div>
  )
}

function ProjectSettingsSkeleton() {
  return (
    <div className="space-y-6">
      <div>
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-4 w-96 mt-2" />
      </div>
      
      <Card>
        <CardHeader>
          <Skeleton className="h-6 w-32" />
          <Skeleton className="h-4 w-64" />
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Skeleton className="h-4 w-24 mb-2" />
            <Skeleton className="h-10 w-full" />
          </div>
          <div>
            <Skeleton className="h-4 w-32 mb-2" />
            <Skeleton className="h-10 w-full" />
          </div>
          <Skeleton className="h-10 w-32" />
        </CardContent>
      </Card>
    </div>
  )
}