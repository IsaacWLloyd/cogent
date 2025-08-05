import { useState, useEffect } from 'react'
import DynamicTerminalCTA, { TerminalState } from './DynamicTerminalCTA'

const phrases = [
  "English is the final programming language.",
  "Cogent implements its full potential."
]

interface TypingAnimationProps {
  onCTAShow?: () => void
}

export default function TypingAnimation({ onCTAShow }: TypingAnimationProps) {
  const [currentPhraseIndex, setCurrentPhraseIndex] = useState(0)
  const [currentText, setCurrentText] = useState("")
  const [isTyping, setIsTyping] = useState(true)
  const [charIndex, setCharIndex] = useState(0)
  const [showPrompt, setShowPrompt] = useState(true)
  const [showCTA, setShowCTA] = useState(false)
  const [sunAscii, setSunAscii] = useState<string[]>([])
  const [opacity, setOpacity] = useState(1)

  // Handle scroll-based fade out
  useEffect(() => {
    const handleScroll = () => {
      const scrollY = window.scrollY
      const windowHeight = window.innerHeight
      const fadeStart = windowHeight * 0.1 // Start fading at 10% of viewport height
      const fadeEnd = windowHeight * 0.27  // Fully faded at 27% of viewport height (3x faster fade)
      
      if (scrollY <= fadeStart) {
        setOpacity(1)
      } else if (scrollY >= fadeEnd) {
        setOpacity(0)
      } else {
        const fadeRange = fadeEnd - fadeStart
        const fadeProgress = (scrollY - fadeStart) / fadeRange
        setOpacity(1 - fadeProgress)
      }
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // Load sun ASCII art
  useEffect(() => {
    fetch('/sun-ascii.txt')
      .then(res => res.text())
      .then(text => {
        setSunAscii(text.split('\n'))
      })
      .catch(err => console.error('Failed to load sun ASCII art:', err))
  }, [])

  // Hero terminal states (smaller version of FinalSection)
  const heroTerminalStates: TerminalState[] = [
    {
      type: 'static',
      content: sunAscii,
      duration: 1000 // Show sun ASCII for 1 second
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
      duration: 1200
    },
    {
      type: 'input',
      content: "Do not get left behind.",
      placeholder: "example@gmail.com",
      onSubmit: (email) => {
        console.log("Hero waitlist signup:", email)
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

  useEffect(() => {
    // Show prompt for 1.5 seconds before starting
    if (showPrompt) {
      const timeout = setTimeout(() => {
        setShowPrompt(false)
      }, 1500)
      
      return () => clearTimeout(timeout)
    }

    const currentPhrase = phrases[currentPhraseIndex]
    
    if (isTyping) {
      // Typing phase
      if (charIndex < currentPhrase.length) {
        const timeout = setTimeout(() => {
          setCurrentText(currentPhrase.slice(0, charIndex + 1))
          setCharIndex(charIndex + 1)
        }, 75) // 75ms per character typing (25% faster)
        
        return () => clearTimeout(timeout)
      } else {
        // Finished typing, wait before starting to delete
        const timeout = setTimeout(() => {
          if (currentPhraseIndex === phrases.length - 1) {
            // Last phrase - show CTA after 300ms delay
            setTimeout(() => {
              setShowCTA(true)
              onCTAShow?.()
            }, 300)
            return
          }
          setIsTyping(false)
        }, 2000) // Wait 2 seconds before deleting
        
        return () => clearTimeout(timeout)
      }
    } else {
      // Deleting phase
      if (charIndex > 0) {
        const timeout = setTimeout(() => {
          setCurrentText(currentPhrase.slice(0, charIndex - 1))
          setCharIndex(charIndex - 1)
        }, 25) // 25ms per character deletion (much faster)
        
        return () => clearTimeout(timeout)
      } else {
        // Finished deleting, move to next phrase
        setCurrentPhraseIndex((prev) => (prev + 1) % phrases.length)
        setIsTyping(true)
      }
    }
  }, [charIndex, currentPhraseIndex, isTyping, showPrompt])

  return (
    <div className="flex flex-col items-center justify-center space-y-8 transition-opacity duration-300" style={{ opacity }}>
      {/* Mobile: Centered multiline wrapper */}
      <div className="sm:hidden text-center max-w-xs">
        <span className="font-mono text-lg text-white bg-black px-4 py-2 leading-relaxed inline-block">
          {showPrompt ? ">" : currentText}
          {/* Blinking cursor */}
          <span className="animate-pulse">|</span>
        </span>
      </div>
      
      {/* Desktop: Single line left-justified */}
      <div className="hidden sm:inline-block">
        <span className="font-mono text-2xl md:text-3xl lg:text-4xl xl:text-5xl text-white bg-black px-4 py-2">
          {showPrompt ? ">" : currentText}
          {/* Blinking cursor */}
          <span className="animate-pulse">|</span>
        </span>
      </div>
      
      {/* Terminal CTA */}
      <DynamicTerminalCTA 
        states={heroTerminalStates}
        systemColor="#ECCD8C"
        isVisible={showCTA}
        visibilityTrigger="manual"
        size="small"
      />
    </div>
  )
}
