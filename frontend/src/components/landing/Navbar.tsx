import { useEffect, useState } from "react"

interface NavbarProps {
  onOpenTerminal: () => void
}

export default function Navbar({ onOpenTerminal }: NavbarProps) {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      const introElement = document.getElementById('intro')
      if (introElement) {
        const rect = introElement.getBoundingClientRect()
        const windowHeight = window.innerHeight
        // Show navbar when IntroSection is about 2/3 up the screen
        // This means when only 1/3 of the viewport height remains below the top of the section
        setIsVisible(rect.top <= windowHeight * 0.33)
      }
    }

    window.addEventListener('scroll', handleScroll)
    handleScroll() // Check initial state
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 bg-neutral-950 border-b border-white/20 transition-transform duration-300 ${
      isVisible ? 'translate-y-0' : '-translate-y-full'
    }`}>
      <div className="flex h-16 items-center justify-between px-4 sm:px-6 max-w-7xl mx-auto relative">
        {/* Logo positioned slightly outside left boundary */}
        <a href="/" className="absolute left-2 sm:left-4">
          <img 
            src="/cogent-logo.svg" 
            alt="Cogent" 
            className="h-10 sm:h-12 w-auto"
          />
        </a>
        
        {/* Get Access button positioned slightly outside right boundary */}
        <div className="absolute right-2 sm:right-4">
          <button
            onClick={onOpenTerminal}
            className="bg-black border border-white/20 text-white hover:bg-neutral-900 text-sm px-4 py-2 rounded-sm transition-colors"
            style={{ fontFamily: 'Kode Mono, monospace' }}
          >
            Get access
          </button>
        </div>
      </div>
    </nav>
  )
}