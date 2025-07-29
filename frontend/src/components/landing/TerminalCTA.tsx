import { useState, useEffect, useRef } from 'react'

interface TerminalCTAProps {
  isVisible: boolean
}

const loadingMessages = [
  "Initializing system...",
  "Loading kernel modules...",
  "Starting network services...",
  "Mounting file systems...",
  "Checking disk integrity...",
  "Loading user preferences...",
  "Starting daemon processes...",
  "Configuring network interfaces...",
  "Initializing graphics subsystem...",
  "Loading security modules...",
  "System ready.",
  "",
  "Welcome to Cogent OS v1.0.0",
  ""
]

export default function TerminalCTA({ isVisible }: TerminalCTAProps) {
  const [phase, setPhase] = useState<'loading' | 'input' | 'success'>('loading')
  const [displayedLines, setDisplayedLines] = useState<string[]>([])
  const [currentLineIndex, setCurrentLineIndex] = useState(0)
  const [email, setEmail] = useState('')
  const [showCursor, setShowCursor] = useState(true)
  const [hasStarted, setHasStarted] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)
  const terminalRef = useRef<HTMLDivElement>(null)

  // Cursor blink effect
  useEffect(() => {
    const interval = setInterval(() => {
      setShowCursor(prev => !prev)
    }, 530)
    return () => clearInterval(interval)
  }, [])

  // Start loading when visible
  useEffect(() => {
    if (isVisible && !hasStarted) {
      setHasStarted(true)
    }
  }, [isVisible, hasStarted])

  // Loading animation
  useEffect(() => {
    if (!hasStarted || phase !== 'loading') return

    if (currentLineIndex < loadingMessages.length) {
      const timeout = setTimeout(() => {
        setDisplayedLines(prev => [...prev, loadingMessages[currentLineIndex]])
        setCurrentLineIndex(prev => prev + 1)
        
        // Auto-scroll to bottom
        if (terminalRef.current) {
          terminalRef.current.scrollTop = terminalRef.current.scrollHeight
        }
      }, 50) // Very fast scrolling

      return () => clearTimeout(timeout)
    } else {
      // Loading complete, move to input phase
      setTimeout(() => {
        setPhase('input')
        setDisplayedLines([])
      }, 500)
    }
  }, [hasStarted, currentLineIndex, phase])

  // Focus input when entering input phase (with preventScroll to avoid jumping)
  useEffect(() => {
    if (phase === 'input' && inputRef.current) {
      inputRef.current.focus({ preventScroll: true })
    }
  }, [phase])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (email.trim()) {
      setPhase('success')
    }
  }

  // Calculate cursor position
  const getCursorPosition = () => {
    if (!email) return '0ch'
    return `${email.length}ch`
  }

  return (
    <div className={`w-full max-w-xs mx-auto transition-opacity duration-500 ${isVisible ? 'opacity-100' : 'opacity-0'}`}>
      <div 
        ref={terminalRef}
        className="bg-black border border-green-500/30 rounded-sm p-4 font-mono text-sm sm:text-base"
        style={{ minHeight: '200px', maxHeight: '400px', overflowY: 'auto' }}
      >
        {phase === 'loading' && (
          <div className="text-green-500/80">
            {displayedLines.map((line, index) => (
              <div key={index} className="leading-tight">
                {line}
              </div>
            ))}
          </div>
        )}

        {phase === 'input' && (
          <div>
            <div className="text-green-500 mb-4">join us</div>
            <form onSubmit={handleSubmit} className="relative">
              <span className="text-green-500 mr-2">{'>'}</span>
              <div className="inline-block relative">
                <input
                  ref={inputRef}
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="example@gmail.com"
                  className="bg-transparent outline-none text-white placeholder:text-gray-500"
                  style={{ caretColor: 'transparent' }}
                  required
                />
                {showCursor && phase === 'input' && (
                  <span 
                    className="absolute text-green-500 pointer-events-none"
                    style={{ 
                      left: getCursorPosition(),
                      top: '0',
                      transform: 'translateY(-2px)'
                    }}
                  >
                    _
                  </span>
                )}
              </div>
            </form>
          </div>
        )}

        {phase === 'success' && (
          <div>
            <div className="text-green-500 mb-2">Success! Welcome to Cogent.</div>
            <div className="text-green-500 mb-4">Join our community:</div>
            <a 
              href="https://discord.gg/krmUwwNhsp" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-400 underline hover:text-blue-300"
            >
              discord.gg/krmUwwNhsp
            </a>
          </div>
        )}
      </div>
    </div>
  )
}