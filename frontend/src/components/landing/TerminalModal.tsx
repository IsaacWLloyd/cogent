import { useEffect, useState } from 'react'
import DynamicTerminalCTA, { TerminalState } from './DynamicTerminalCTA'

interface TerminalModalProps {
  isOpen: boolean
  onClose: () => void
}

export default function TerminalModal({ isOpen, onClose }: TerminalModalProps) {
  const [sunAscii, setSunAscii] = useState<string[]>([])

  // Load sun ASCII art
  useEffect(() => {
    fetch('/sun-ascii.txt')
      .then(res => res.text())
      .then(text => {
        setSunAscii(text.split('\n'))
      })
      .catch(err => console.error('Failed to load sun ASCII art:', err))
  }, [])

  // Terminal states configuration (same as other instances)
  const modalTerminalStates: TerminalState[] = [
    {
      type: 'static',
      content: sunAscii,
      duration: 500 // Show sun ASCII for 500ms
    },
    {
      type: 'scrolling',
      content: [
        "Starting kernel...",
        "Initializing linguistic object framework...",
        "Loading brain-picking protocols...",
        "Checking PCI devices...",
        "Mounting ideaspace exploration modules...",
        "Starting agent compliance enforcement...",
        "Loading collective unconscious drivers...",
        "Initializing hierarchical specification trees...",
        "Detecting shadow projection algorithms...",
        "Loading dynamic context management...",
        "Mounting /dev/anima and /dev/animus...",
        "Crystallizing intention capture systems...",
        "Starting blueprint synthesis engine...",
        "Loading archetypal pattern recognition...",
        "Validating thought-to-code pipelines...",
        "Starting individuation processes...",
        "Loading Platonic form databases...",
        "Mounting cave wall renderer...",
        "Initializing eternal realm interfaces...",
        "Loading the world of forms...",
        "Starting transcendence acceleration protocols...",
        "Activating consciousness elevation frameworks...",
        "Loading ego dissolution subroutines...",
        "Mounting unity consciousness drivers...",
        "Starting network daemon...",
        "Initializing symbolic synchronicity engine...",
        "Loading mandala geometry processors...",
        "Agent drift eliminated.",
        "Context preserved.",
        "Vision intact.",
        "Shadows integrated.",
        "Forms realized.",
        "",
        "Welcome to Cogent OS v1.0.0",
        "English is the final programming language.",
        "The cave wall dissolves.",
        ""
      ],
      duration: 1200 // Total time for all lines to scroll
    },
    {
      type: 'input',
      content: "Your unfair advantage.",
      placeholder: "example@gmail.com",
      onSubmit: (email) => {
        console.log("Modal waitlist signup:", email)
        // TODO: Handle waitlist signup
      }
    },
    {
      type: 'link',
      content: [],
      linkUrl: "https://discord.gg/krmUwwNhsp",
      linkText: "discord.gg/krmUwwNhsp",
      linkDescription: "Where it all happens."
    }
  ]

  // Close modal on Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose()
      }
    }

    if (isOpen) {
      document.addEventListener('keydown', handleEscape)
      return () => document.removeEventListener('keydown', handleEscape)
    }
  }, [isOpen, onClose])

  if (!isOpen) return null

  return (
    <div 
      className="fixed inset-0 z-[9999]"
      style={{ backgroundColor: 'rgba(0, 0, 0, 0.9)' }}
      onClick={(e) => {
        // Close modal when clicking overlay (but not the terminal)
        if (e.target === e.currentTarget) {
          onClose()
        }
      }}
    >
      {/* Absolutely positioned container to avoid flex interference */}
      <div 
        className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
      >
        {/* Close button - smaller box */}
        <button
          onClick={onClose}
          className="absolute top-1 right-1 z-10 w-4 h-4 bg-transparent hover:bg-white/10 text-white rounded transition-colors flex items-center justify-center text-sm font-bold"
        >
          ×
        </button>
        
        {/* Large Terminal - no flex interference */}
        <DynamicTerminalCTA 
          states={modalTerminalStates}
          systemColor="#ECCD8C"
          alwaysVisible={true}
          size="large"
        />
      </div>
    </div>
  )
}