import { create } from 'zustand'
import type { Document } from '@shared/types'

interface DocumentState {
  selectedDocument: Document | null
  searchQuery: string
  searchResults: Document[]
  
  // Actions
  setSelectedDocument: (document: Document | null) => void
  setSearchQuery: (query: string) => void
  setSearchResults: (results: Document[]) => void
}

export const useDocumentStore = create<DocumentState>((set) => ({
  selectedDocument: null,
  searchQuery: '',
  searchResults: [],

  setSelectedDocument: (document) => {
    set({ selectedDocument: document })
  },

  setSearchQuery: (query) => {
    set({ searchQuery: query })
  },

  setSearchResults: (results) => {
    set({ searchResults: results })
  },
}))