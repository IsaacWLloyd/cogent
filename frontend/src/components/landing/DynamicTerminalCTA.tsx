import { useState, useEffect, useRef } from 'react'

// Types for different terminal states
export interface BaseTerminalState {
  type: 'static' | 'scrolling' | 'input' | 'link'
  content: string | string[] // string for single line, string[] for multiple lines
}

export interface StaticState extends BaseTerminalState {
  type: 'static'
  duration: number // milliseconds
}

export interface ScrollingState extends BaseTerminalState {
  type: 'scrolling'
  duration: number // total duration for all lines to scroll
}

export interface InputState extends BaseTerminalState {
  type: 'input'
  placeholder?: string
  onSubmit?: (value: string) => Promise<{ success: boolean; message: string }> | void
  successMessage?: string | string[]
}

export interface LinkState extends BaseTerminalState {
  type: 'link'
  linkUrl: string
  linkText: string
  linkDescription?: string // optional text above the link
  duration?: number // optional duration before auto-advancing
}

export type TerminalState = StaticState | ScrollingState | InputState | LinkState

export type TerminalSize = 'small' | 'medium' | 'large'

export interface DynamicTerminalCTAProps {
  states: TerminalState[]
  systemColor?: string // hex color, defaults to #10b981 (green-500)
  alwaysVisible?: boolean // if true, component is always visible
  visibilityTrigger?: 'scroll' | 'manual' // how visibility is triggered
  isVisible?: boolean // for manual visibility control
  className?: string
  size?: TerminalSize // terminal size preset
  onComplete?: () => void // callback when all states are complete
}

export default function DynamicTerminalCTA({
  states,
  systemColor = '#10b981',
  alwaysVisible = false,
  visibilityTrigger = 'scroll',
  isVisible: manualVisible = false,
  className = '',
  size = 'medium',
  onComplete
}: DynamicTerminalCTAProps) {
  const [currentStateIndex, setCurrentStateIndex] = useState(0)
  const [displayedLines, setDisplayedLines] = useState<string[]>([])
  const [currentLineIndex, setCurrentLineIndex] = useState(0)
  const [inputValue, setInputValue] = useState('')
  const [showCursor, setShowCursor] = useState(true)
  const [isInView, setIsInView] = useState(false)
  const [hasStarted, setHasStarted] = useState(false)
  const [statePhase, setStatePhase] = useState<'active' | 'complete'>('active')
  
  const terminalRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  const currentState = states[currentStateIndex]
  const isVisible = alwaysVisible || (visibilityTrigger === 'manual' ? manualVisible : isInView)
  
  // Detect 4K screens and adjust sizing
  const is4K = typeof window !== 'undefined' && (window.innerWidth >= 3840 || window.innerHeight >= 2160)
  
  // Size configurations
  const getSizeConfig = (size: TerminalSize) => {
    const baseConfigs = {
      small: {
        containerMaxWidth: 'max-w-sm', // 384px
        height: '200px',
        fontSize: 'text-xs sm:text-sm',
        padding: 'p-3'
      },
      medium: {
        containerMaxWidth: 'max-w-2xl', // 672px  
        height: '400px',
        fontSize: 'text-sm sm:text-base',
        padding: 'p-4'
      },
      large: {
        containerMaxWidth: 'max-w-4xl', // 896px
        height: '600px', 
        fontSize: 'text-base sm:text-lg',
        padding: 'p-6'
      }
    }
    
    const config = baseConfigs[size]
    
    // Scale up for 4K screens
    if (is4K) {
      return {
        ...config,
        containerMaxWidth: size === 'small' ? 'max-w-lg' : size === 'medium' ? 'max-w-4xl' : 'max-w-6xl',
        height: size === 'small' ? '300px' : size === 'medium' ? '600px' : '800px',
        fontSize: size === 'small' ? 'text-sm sm:text-base' : size === 'medium' ? 'text-base sm:text-lg' : 'text-lg sm:text-xl'
      }
    }
    
    return config
  }
  
  const sizeConfig = getSizeConfig(size)
  
  // Convert content to array if it's a string
  const getContentArray = (content: string | string[]): string[] => {
    return Array.isArray(content) ? content : [content]
  }

  // Cursor blink effect
  useEffect(() => {
    const interval = setInterval(() => {
      setShowCursor(prev => !prev)
    }, 530)
    return () => clearInterval(interval)
  }, [])

  // Intersection observer - always track when component is in view
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsInView(true)
          }
        })
      },
      { threshold: 0.5 }
    )

    if (containerRef.current) {
      observer.observe(containerRef.current)
    }

    return () => {
      if (containerRef.current) {
        observer.unobserve(containerRef.current)
      }
    }
  }, [])

  // Start processing when visible AND in view (even if alwaysVisible is true)
  useEffect(() => {
    if (isVisible && isInView && !hasStarted) {
      setHasStarted(true)
    }
  }, [isVisible, isInView, hasStarted])

  // Handle state transitions
  useEffect(() => {
    if (!hasStarted || !currentState) return

    if (currentState.type === 'static') {
      // Display all content immediately
      setDisplayedLines(getContentArray(currentState.content))
      
      // Set timer for next state
      const timer = setTimeout(() => {
        moveToNextState()
      }, currentState.duration)

      return () => clearTimeout(timer)
    }

    if (currentState.type === 'scrolling') {
      const lines = getContentArray(currentState.content)
      const timePerLine = currentState.duration / lines.length

      if (currentLineIndex < lines.length) {
        const timer = setTimeout(() => {
          setDisplayedLines(prev => [...prev, lines[currentLineIndex]])
          setCurrentLineIndex(prev => prev + 1)
          
          // Auto-scroll
          if (terminalRef.current) {
            terminalRef.current.scrollTop = terminalRef.current.scrollHeight
          }
        }, timePerLine)

        return () => clearTimeout(timer)
      } else {
        // Scrolling complete, move to next state
        moveToNextState()
      }
    }

    if (currentState.type === 'link' && currentState.duration) {
      // Display content immediately
      setDisplayedLines(getContentArray(currentState.content))
      
      // Optional auto-advance
      const timer = setTimeout(() => {
        moveToNextState()
      }, currentState.duration)

      return () => clearTimeout(timer)
    }

    if (currentState.type === 'input' || currentState.type === 'link') {
      // Display content immediately for input/link states
      setDisplayedLines(getContentArray(currentState.content))
      
      // Focus input if it's an input state (with preventScroll to avoid jumping)
      if (currentState.type === 'input' && inputRef.current && statePhase === 'active') {
        inputRef.current.focus({ preventScroll: true })
      }
    }
  }, [hasStarted, currentState, currentLineIndex, statePhase])

  const moveToNextState = () => {
    if (currentStateIndex < states.length - 1) {
      setCurrentStateIndex(prev => prev + 1)
      setDisplayedLines([])
      setCurrentLineIndex(0)
      setStatePhase('active')
      setInputValue('')
    } else {
      onComplete?.()
    }
  }

  const handleInputSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputValue.trim()) return

    const inputState = currentState as InputState
    
    // Clear the input state content immediately
    setDisplayedLines([])
    
    // Show loading state
    setStatePhase('complete')
    setDisplayedLines(['Processing...'])
    
    try {
      let result
      
      // Check if it's an email input (simple validation)
      if (inputValue.includes('@')) {
        // Save email to database
        try {
          const response = await fetch('/api/v1/waitlist', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: inputValue })
          });
          
          const data = await response.json();
          
          if (!response.ok) {
            throw new Error(data.error || 'Failed to join waitlist');
          }
          
          result = { success: true, message: data.message };
        } catch (error) {
          console.error('Waitlist signup error:', error);
          result = { 
            success: false, 
            message: error instanceof Error ? error.message : 'Failed to join waitlist' 
          };
        }
      } else {
        // For non-email inputs, use the provided onSubmit handler
        result = await inputState.onSubmit?.(inputValue)
      }
      
      if (result) {
        // Show the response message
        setDisplayedLines([result.message])
        
        // Auto-advance after showing message
        setTimeout(() => {
          moveToNextState()
        }, result.success ? 2000 : 3000)
      } else if (inputState.successMessage) {
        // Fallback to static success message
        setDisplayedLines(getContentArray(inputState.successMessage))
        setTimeout(() => {
          moveToNextState()
        }, 2000)
      } else {
        moveToNextState()
      }
    } catch (error) {
      // Show error message
      setDisplayedLines(['Error: Failed to process request'])
      setTimeout(() => {
        moveToNextState()
      }, 3000)
    }
  }

  // Calculate cursor position for input
  const getCursorPosition = () => {
    if (!inputValue) return '0ch'
    return `${inputValue.length}ch`
  }

  const shouldShowContent = alwaysVisible || isVisible

  return (
    <div 
      ref={containerRef}
      className={`w-full ${sizeConfig.containerMaxWidth} mx-auto transition-opacity duration-500 ${shouldShowContent ? 'opacity-100' : 'opacity-0'} ${className}`}
    >
      <div 
        ref={terminalRef}
        className={`bg-black border rounded-sm ${sizeConfig.padding} ${sizeConfig.fontSize} [&::-webkit-scrollbar]:hidden`}
        style={{ 
          fontFamily: 'Kode Mono, monospace',
          borderColor: `${systemColor}30`,
          height: sizeConfig.height, 
          overflowY: 'scroll',
          overflowX: 'hidden',
          scrollbarWidth: 'none', // Firefox
          msOverflowStyle: 'none'  // IE/Edge
        }}
      >
        {/* Display previous lines */}
        {displayedLines.map((line, index) => {
          // Check if this is ASCII art (sun ascii will be the first state)
          const isAsciiArt = currentStateIndex === 0 && currentState?.type === 'static'
          
          // Size-relative ASCII font sizes
          const getAsciiFontSize = () => {
            if (!isAsciiArt) return 'inherit'
            
            const baseSizes = {
              small: '6px',
              medium: '10.4px', 
              large: '12px'
            }
            
            // Scale up for 4K
            if (is4K) {
              return {
                small: '8px',
                medium: '13px',
                large: '15px'
              }[size]
            }
            
            return baseSizes[size]
          }
          
          return (
            <div 
              key={index} 
              className="leading-tight" 
              style={{ 
                color: systemColor, 
                whiteSpace: 'pre',
                fontSize: getAsciiFontSize()
              }}
            >
              {line}
            </div>
          )
        })}

        {/* Current state specific rendering */}
        {currentState && statePhase === 'active' && (
          <>
            {currentState.type === 'input' && (
              <form onSubmit={handleInputSubmit} className="relative mt-2">
                <span style={{ color: systemColor }} className="mr-2">{'>'}</span>
                <div className="inline-block relative">
                  <input
                    ref={inputRef}
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder={(currentState as InputState).placeholder || ''}
                    className="bg-transparent outline-none text-white placeholder:text-gray-500"
                    style={{ caretColor: 'transparent' }}
                  />
                  {showCursor && (
                    <span 
                      className="absolute pointer-events-none"
                      style={{ 
                        color: systemColor,
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
            )}

            {currentState.type === 'link' && (
              <div className="mt-2">
                {(currentState as LinkState).linkDescription && (
                  <div className="mb-2" style={{ color: systemColor }}>
                    {(currentState as LinkState).linkDescription}
                  </div>
                )}
                <a 
                  href={(currentState as LinkState).linkUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="underline hover:opacity-80 transition-opacity"
                  style={{ color: '#8CB9EC' }}
                >
                  {(currentState as LinkState).linkText}
                </a>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}