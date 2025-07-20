import { Routes, Route } from 'react-router-dom'
import { ProtectedRoute } from './components/auth/ProtectedRoute'
import { AuthGuard } from './components/auth/AuthGuard'
import { LoginPage } from './pages/auth/LoginPage'
import { DashboardLayout } from './components/layout/DashboardLayout'
import { DashboardPage } from './pages/dashboard/DashboardPage'
import { ProjectListPage } from './pages/projects/ProjectListPage'
import { ProjectDetailPage } from './pages/projects/ProjectDetailPage'
import { ProjectSettingsPage } from './pages/projects/ProjectSettingsPage'
import { ProfilePage } from './pages/profile/ProfilePage'
import { UsagePage } from './pages/usage/UsagePage'

function App() {
  return (
    <AuthGuard>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <DashboardLayout>
                <Routes>
                  <Route path="/" element={<DashboardPage />} />
                  <Route path="/projects" element={<ProjectListPage />} />
                  <Route path="/projects/:id" element={<ProjectDetailPage />} />
                  <Route path="/projects/:id/settings" element={<ProjectSettingsPage />} />
                  <Route path="/profile" element={<ProfilePage />} />
                  <Route path="/usage" element={<UsagePage />} />
                </Routes>
              </DashboardLayout>
            </ProtectedRoute>
          }
        />
      </Routes>
    </AuthGuard>
  )
}

export default App