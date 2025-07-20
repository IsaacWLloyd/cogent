import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { useProjects } from '@/hooks/useApi'
import { useProjectStore } from '@/stores/projectStore'
import { FileText, Search, Settings, Plus } from 'lucide-react'

export function DashboardPage() {
  const navigate = useNavigate()
  const { data: projectsData, isLoading } = useProjects()
  const { setCurrentProject } = useProjectStore()

  // Auto-select most recent project on dashboard load
  useEffect(() => {
    if (projectsData?.projects && projectsData.projects.length > 0) {
      const mostRecentProject = projectsData.projects[0]
      setCurrentProject(mostRecentProject)
    }
  }, [projectsData, setCurrentProject])

  if (isLoading) {
    return <DashboardSkeleton />
  }

  const projects = projectsData?.projects || []
  const mostRecentProject = projects[0]

  if (projects.length === 0) {
    return <EmptyDashboard />
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome back! Here's your most recent project activity.
        </p>
      </div>

      {/* Recent Project Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            {mostRecentProject.name}
          </CardTitle>
          <CardDescription>
            Last updated {new Date(mostRecentProject.createdAt).toLocaleDateString()}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2">
            <Button 
              onClick={() => navigate(`/projects/${mostRecentProject.id}`)}
            >
              <FileText className="mr-2 h-4 w-4" />
              View Documents
            </Button>
            <Button 
              variant="outline"
              onClick={() => navigate(`/projects/${mostRecentProject.id}/settings`)}
            >
              <Settings className="mr-2 h-4 w-4" />
              Settings
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card className="cursor-pointer hover:shadow-md transition-shadow"
              onClick={() => navigate('/projects')}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              All Projects
            </CardTitle>
            <CardDescription>
              View and manage all your projects
            </CardDescription>
          </CardHeader>
        </Card>

        <Card className="cursor-pointer hover:shadow-md transition-shadow"
              onClick={() => navigate(`/projects/${mostRecentProject.id}`)}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Search className="h-5 w-5" />
              Search Documents
            </CardTitle>
            <CardDescription>
              Find specific documentation quickly
            </CardDescription>
          </CardHeader>
        </Card>

        <Card className="cursor-pointer hover:shadow-md transition-shadow"
              onClick={() => navigate('/profile')}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Settings className="h-5 w-5" />
              Profile Settings
            </CardTitle>
            <CardDescription>
              Manage your account and preferences
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    </div>
  )
}

function DashboardSkeleton() {
  return (
    <div className="space-y-6">
      <div>
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-4 w-96 mt-2" />
      </div>
      <Card>
        <CardHeader>
          <Skeleton className="h-6 w-32" />
          <Skeleton className="h-4 w-48" />
        </CardHeader>
        <CardContent>
          <div className="flex gap-2">
            <Skeleton className="h-10 w-32" />
            <Skeleton className="h-10 w-24" />
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

function EmptyDashboard() {
  const navigate = useNavigate()

  return (
    <div className="text-center space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Welcome to COGENT</h1>
        <p className="text-muted-foreground mt-2">
          Get started by creating your first project
        </p>
      </div>
      <Card className="max-w-md mx-auto">
        <CardHeader>
          <CardTitle>No Projects Yet</CardTitle>
          <CardDescription>
            Create your first project to start generating and managing documentation
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button onClick={() => navigate('/projects')} className="w-full">
            <Plus className="mr-2 h-4 w-4" />
            Create Project
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}