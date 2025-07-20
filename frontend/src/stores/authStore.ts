import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import type { User, AuthProvider } from '@shared/types'
import { api } from '@/lib/api'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  
  // Actions
  setUser: (user: User | null) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  login: (provider: AuthProvider) => void
  logout: () => Promise<void>
  checkAuth: () => Promise<void>
  refreshToken: () => Promise<boolean>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      setUser: (user) => {
        set({ 
          user, 
          isAuthenticated: !!user,
          error: null 
        })
      },

      setLoading: (isLoading) => {
        set({ isLoading })
      },

      setError: (error) => {
        set({ error })
      },

      login: (provider) => {
        // Redirect to backend OAuth endpoint
        window.location.href = `/api/v1/auth/login?provider=${provider}`
      },

      logout: async () => {
        try {
          set({ isLoading: true, error: null })
          await api.logout()
          set({ 
            user: null, 
            isAuthenticated: false, 
            isLoading: false 
          })
        } catch (error) {
          console.error('Logout failed:', error)
          // Still clear local state even if API call fails
          set({ 
            user: null, 
            isAuthenticated: false, 
            isLoading: false,
            error: error instanceof Error ? error.message : 'Logout failed'
          })
        }
      },

      checkAuth: async () => {
        try {
          set({ isLoading: true, error: null })
          const user = await api.getProfile()
          set({ 
            user, 
            isAuthenticated: true, 
            isLoading: false 
          })
        } catch (error) {
          set({ 
            user: null, 
            isAuthenticated: false, 
            isLoading: false,
            error: error instanceof Error ? error.message : 'Authentication check failed'
          })
        }
      },

      refreshToken: async () => {
        try {
          await api.refreshToken()
          // Token refresh successful, auth state remains valid
          return true
        } catch (error) {
          // Refresh failed, clear auth state
          set({ 
            user: null, 
            isAuthenticated: false,
            error: 'Session expired'
          })
          return false
        }
      },
    }),
    {
      name: 'auth-store',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ 
        user: state.user,
        isAuthenticated: state.isAuthenticated 
      }),
    }
  )
)