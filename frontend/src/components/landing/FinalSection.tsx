import { useState, useEffect, useRef } from 'react'
import DynamicTerminalCTA, { TerminalState } from './DynamicTerminalCTA'

export default function FinalSection() {
  const [hasBeenVisible, setHasBeenVisible] = useState(false)
  const [sunAscii, setSunAscii] = useState<string[]>([])
  const sectionRef = useRef<HTMLElement>(null)

  // Load sun ASCII art
  useEffect(() => {
    fetch('/sun-ascii.txt')
      .then(res => res.text())
      .then(text => {
        setSunAscii(text.split('\n'))
      })
      .catch(err => console.error('Failed to load sun ASCII art:', err))
  }, [])

  // Terminal states configuration
  const terminalStates: TerminalState[] = [
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
      content: "Don't get left behind.",
      placeholder: "example@gmail.com",
      // Email submission is now handled automatically by DynamicTerminalCTA
    },
    {
      type: 'link',
      content: [],
      linkUrl: "https://discord.gg/krmUwwNhsp",
      linkText: "discord.gg/krmUwwNhsp",
      linkDescription: "Where it all happens."
    }
  ]

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !hasBeenVisible) {
            setHasBeenVisible(true)
            // Wait 1 second after section comes into view
            setTimeout(() => {
              // Terminal is always visible, no need to set state
            }, 1000)
          }
        })
      },
      {
        threshold: 0.5 // Trigger when 50% of the section is visible
      }
    )

    if (sectionRef.current) {
      observer.observe(sectionRef.current)
    }

    return () => {
      if (sectionRef.current) {
        observer.unobserve(sectionRef.current)
      }
    }
  }, [hasBeenVisible])

  return (
    <section ref={sectionRef} className="w-full bg-neutral-950/0 py-32">
      <div className="w-full flex flex-col items-center justify-center space-y-12">
        {/* Dynamic Terminal CTA */}
        <DynamicTerminalCTA 
          states={terminalStates}
          systemColor="#ECCD8C"
          alwaysVisible={true}
          size="medium"
        />
      </div>
    </section>
  )
}