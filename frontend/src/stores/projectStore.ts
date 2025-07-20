import { create } from 'zustand'
import type { Project } from '@shared/types'

interface ProjectState {
  currentProject: Project | null
  selectedProjectId: string | null
  
  // Actions
  setCurrentProject: (project: Project | null) => void
  setSelectedProjectId: (id: string | null) => void
}

export const useProjectStore = create<ProjectState>((set) => ({
  currentProject: null,
  selectedProjectId: null,

  setCurrentProject: (project) => {
    set({ 
      currentProject: project,
      selectedProjectId: project?.id || null
    })
  },

  setSelectedProjectId: (id) => {
    set({ selectedProjectId: id })
  },
}))