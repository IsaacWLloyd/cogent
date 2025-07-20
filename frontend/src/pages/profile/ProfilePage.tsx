import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Skeleton } from '@/components/ui/skeleton'
import { useUser, useUpdateUser } from '@/hooks/useApi'
import { useAuthStore } from '@/stores/authStore'
import { Save, LogOut, User, Mail } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

export function ProfilePage() {
  const { data: user, isLoading } = useUser()
  const updateUser = useUpdateUser()
  const { logout } = useAuthStore()
  const { toast } = useToast()
  
  const [formData, setFormData] = useState({
    name: '',
  })

  // Update form when user loads
  useEffect(() => {
    if (user) {
      setFormData({
        name: user.name || '',
      })
    }
  }, [user])

  const handleSave = async () => {
    try {
      await updateUser.mutateAsync({
        name: formData.name.trim() || null,
      })
      
      toast({
        title: "Profile updated",
        description: "Your profile has been saved successfully.",
      })
    } catch (error) {
      toast({
        title: "Update failed",
        description: "There was an error updating your profile.",
        variant: "destructive",
      })
    }
  }

  const handleLogout = async () => {
    try {
      await logout()
      toast({
        title: "Logged out",
        description: "You have been successfully logged out.",
      })
    } catch (error) {
      toast({
        title: "Logout failed",
        description: "There was an error logging you out.",
        variant: "destructive",
      })
    }
  }

  if (isLoading) {
    return <ProfileSkeleton />
  }

  if (!user) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold">Profile Not Found</h1>
        <p className="text-muted-foreground mt-2">
          Unable to load your profile information.
        </p>
      </div>
    )
  }

  const initials = user.name 
    ? user.name.split(' ').map(n => n[0]).join('').toUpperCase()
    : user.email.charAt(0).toUpperCase()

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Profile</h1>
        <p className="text-muted-foreground">
          Manage your account settings and preferences
        </p>
      </div>

      {/* Profile Info */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-4">
            <Avatar className="h-16 w-16">
              <AvatarFallback className="text-lg">{initials}</AvatarFallback>
            </Avatar>
            <div>
              <h2 className="text-xl font-semibold">
                {user.name || 'No name set'}
              </h2>
              <p className="text-muted-foreground">{user.email}</p>
            </div>
          </CardTitle>
        </CardHeader>
      </Card>

      {/* Basic Information */}
      <Card>
        <CardHeader>
          <CardTitle>Basic Information</CardTitle>
          <CardDescription>
            Update your personal information
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="email">Email Address</Label>
            <div className="flex items-center gap-2">
              <Mail className="h-4 w-4 text-muted-foreground" />
              <Input
                id="email"
                value={user.email}
                disabled
                className="bg-muted"
              />
            </div>
            <p className="text-sm text-muted-foreground mt-1">
              Your email address cannot be changed
            </p>
          </div>
          
          <div>
            <Label htmlFor="name">Display Name</Label>
            <div className="flex items-center gap-2">
              <User className="h-4 w-4 text-muted-foreground" />
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                placeholder="Enter your display name"
              />
            </div>
          </div>
          
          <Button 
            onClick={handleSave}
            disabled={updateUser.isPending}
          >
            <Save className="mr-2 h-4 w-4" />
            {updateUser.isPending ? 'Saving...' : 'Save Changes'}
          </Button>
        </CardContent>
      </Card>

      {/* Account Info */}
      <Card>
        <CardHeader>
          <CardTitle>Account Information</CardTitle>
          <CardDescription>
            Your account details and OAuth connections
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <Label>Account Created</Label>
              <p className="text-sm font-medium">
                {new Date(user.createdAt).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </p>
            </div>
            
            {user.githubId && (
              <div>
                <Label>GitHub Connected</Label>
                <p className="text-sm font-medium text-green-600">
                  ✓ Connected as {user.githubId}
                </p>
              </div>
            )}
            
            {user.googleId && (
              <div>
                <Label>Google Connected</Label>
                <p className="text-sm font-medium text-green-600">
                  ✓ Connected as {user.googleId}
                </p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Logout */}
      <Card>
        <CardHeader>
          <CardTitle>Session</CardTitle>
          <CardDescription>
            Manage your current session
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button variant="outline" onClick={handleLogout}>
            <LogOut className="mr-2 h-4 w-4" />
            Sign Out
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}

function ProfileSkeleton() {
  return (
    <div className="space-y-6">
      <div>
        <Skeleton className="h-8 w-24" />
        <Skeleton className="h-4 w-64 mt-2" />
      </div>
      
      <Card>
        <CardHeader>
          <div className="flex items-center gap-4">
            <Skeleton className="h-16 w-16 rounded-full" />
            <div>
              <Skeleton className="h-6 w-32" />
              <Skeleton className="h-4 w-48 mt-2" />
            </div>
          </div>
        </CardHeader>
      </Card>
      
      <Card>
        <CardHeader>
          <Skeleton className="h-6 w-32" />
          <Skeleton className="h-4 w-48" />
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Skeleton className="h-4 w-24 mb-2" />
            <Skeleton className="h-10 w-full" />
          </div>
          <div>
            <Skeleton className="h-4 w-24 mb-2" />
            <Skeleton className="h-10 w-full" />
          </div>
          <Skeleton className="h-10 w-32" />
        </CardContent>
      </Card>
    </div>
  )
}