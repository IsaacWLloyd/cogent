import { useLocation, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { useProjects } from '@/hooks/useApi'
import { useProjectStore } from '@/stores/projectStore'
import { cn } from '@/lib/utils'
import { 
  Home, 
  FolderOpen, 
  Plus, 
  Settings,
  FileText,
  BarChart3
} from 'lucide-react'

export function Sidebar() {
  const navigate = useNavigate()
  const location = useLocation()
  const { data: projectsData, isLoading } = useProjects()
  const { currentProject, setCurrentProject } = useProjectStore()

  const projects = projectsData?.projects || []

  const navigationItems = [
    {
      label: 'Dashboard',
      href: '/',
      icon: Home,
      isActive: location.pathname === '/',
    },
    {
      label: 'All Projects',
      href: '/projects',
      icon: FolderOpen,
      isActive: location.pathname === '/projects',
    },
    {
      label: 'Usage & Billing',
      href: '/usage',
      icon: BarChart3,
      isActive: location.pathname === '/usage',
    },
  ]

  const handleProjectSelect = (project: typeof projects[0]) => {
    setCurrentProject(project)
    navigate(`/projects/${project.id}`)
  }

  return (
    <div className="w-64 border-r bg-background flex flex-col h-screen">
      {/* Logo/Brand */}
      <div className="p-6">
        <h1 className="text-xl font-bold">COGENT</h1>
        <p className="text-sm text-muted-foreground">Code Documentation</p>
      </div>

      <div className="flex-1 px-4 space-y-4">
        {/* Main Navigation */}
        <nav className="space-y-1">
          {navigationItems.map((item) => (
            <Button
              key={item.href}
              variant={item.isActive ? 'secondary' : 'ghost'}
              className={cn(
                'w-full justify-start',
                item.isActive && 'bg-secondary'
              )}
              onClick={() => navigate(item.href)}
            >
              <item.icon className="mr-2 h-4 w-4" />
              {item.label}
            </Button>
          ))}
        </nav>

        <Separator />

        {/* Projects Section */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-muted-foreground">Projects</h3>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate('/projects')}
            >
              <Plus className="h-4 w-4" />
            </Button>
          </div>

          <div className="space-y-1">
            {isLoading ? (
              <ProjectListSkeleton />
            ) : projects.length === 0 ? (
              <div className="text-center py-4">
                <p className="text-sm text-muted-foreground">No projects yet</p>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => navigate('/projects')}
                  className="mt-2"
                >
                  <Plus className="mr-2 h-4 w-4" />
                  Create Project
                </Button>
              </div>
            ) : (
              projects.map((project) => {
                const isCurrentProject = currentProject?.id === project.id
                const isOnProjectPage = location.pathname.startsWith(`/projects/${project.id}`)
                
                return (
                  <div key={project.id} className="space-y-1">
                    <Button
                      variant={isOnProjectPage ? 'secondary' : 'ghost'}
                      className={cn(
                        'w-full justify-start text-left',
                        isOnProjectPage && 'bg-secondary'
                      )}
                      onClick={() => handleProjectSelect(project)}
                    >
                      <FileText className="mr-2 h-4 w-4 flex-shrink-0" />
                      <span className="truncate flex-1">{project.name}</span>
                      {isCurrentProject && (
                        <Badge variant="secondary" className="ml-2 text-xs">
                          Active
                        </Badge>
                      )}
                    </Button>
                    
                    {/* Project Sub-navigation */}
                    {isOnProjectPage && (
                      <div className="ml-6 space-y-1">
                        <Button
                          variant="ghost"
                          size="sm"
                          className={cn(
                            'w-full justify-start text-xs',
                            location.pathname === `/projects/${project.id}` && 'bg-muted'
                          )}
                          onClick={() => navigate(`/projects/${project.id}`)}
                        >
                          Documents
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          className={cn(
                            'w-full justify-start text-xs',
                            location.pathname === `/projects/${project.id}/settings` && 'bg-muted'
                          )}
                          onClick={() => navigate(`/projects/${project.id}/settings`)}
                        >
                          Settings
                        </Button>
                      </div>
                    )}
                  </div>
                )
              })
            )}
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 border-t">
        <Button
          variant="ghost"
          size="sm"
          className="w-full justify-start"
          onClick={() => navigate('/profile')}
        >
          <Settings className="mr-2 h-4 w-4" />
          Settings
        </Button>
      </div>
    </div>
  )
}

function ProjectListSkeleton() {
  return (
    <div className="space-y-1">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="flex items-center space-x-2 p-2">
          <Skeleton className="h-4 w-4" />
          <Skeleton className="h-4 flex-1" />
        </div>
      ))}
    </div>
  )
}