import { useEffect, useState } from 'react'

export default function StickyWallpaper() {
  const [scrollY, setScrollY] = useState(0)
  const [fontSize, setFontSize] = useState(1)
  const [asciiArt, setAsciiArt] = useState('')

  // Load ASCII art from file
  useEffect(() => {
    fetch('/ascii-art.txt')
      .then(res => res.text())
      .then(text => setAsciiArt(text))
      .catch(err => console.error('Failed to load ASCII art:', err))
  }, [])

  // Handle scroll
  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // Calculate font size to match image dimensions
  useEffect(() => {
    if (!asciiArt) return

    const calculateFontSize = () => {
      const asciiLines = asciiArt.split('\n')
      const asciiHeight = asciiLines.length
      const asciiWidth = Math.max(...asciiLines.map(line => line.length))
      
      // Get viewport dimensions
      const viewportWidth = window.innerWidth
      const viewportHeight = window.innerHeight
      const viewportAspectRatio = viewportWidth / viewportHeight
      
      // Hero image aspect ratio (you may need to adjust this based on your actual image)
      const imageAspectRatio = 1.78 // approximately 16:9
      
      // Character dimensions for monospace font
      const charWidthRatio = 0.6
      const lineHeightRatio = 1.2
      
      // Calculate font size to match the hero image scaling behavior
      let fontSize
      if (viewportAspectRatio > imageAspectRatio) {
        // Viewport is wider than image - background-size: 100% auto
        // Image fills width, height may overflow
        fontSize = viewportWidth / (asciiWidth * charWidthRatio)
      } else {
        // Viewport is taller than image - background-size: auto 100%
        // Image fills height, width may overflow
        fontSize = viewportHeight / (asciiHeight * lineHeightRatio)
      }
      
      setFontSize(Math.max(fontSize, 1))
    }
    
    calculateFontSize()
    window.addEventListener('resize', calculateFontSize)
    return () => window.removeEventListener('resize', calculateFontSize)
  }, [asciiArt])

  // Calculate crossfade opacities
  const maxScroll = typeof window !== 'undefined' ? window.innerHeight : 1000
  const scrollProgress = Math.min(scrollY / maxScroll, 1)
  const imageOpacity = 1 - scrollProgress
  const asciiOpacity = scrollProgress

  // Determine background size based on viewport aspect ratio
  const viewportAspectRatio = typeof window !== 'undefined' 
    ? window.innerWidth / window.innerHeight 
    : 16/9
  const imageAspectRatio = 1.78 // approximately 16:9
  
  return (
    <div className="fixed inset-0 w-full h-full overflow-hidden">
      {/* Hero Image - fills screen and overflows as needed */}
      <div 
        className="absolute inset-0 w-full h-full transition-opacity duration-300 ease-out"
        style={{
          backgroundImage: 'url(/cogent-hero-no-watermark.png)',
          backgroundPosition: 'center center',
          backgroundRepeat: 'no-repeat',
          backgroundSize: viewportAspectRatio > imageAspectRatio 
            ? '100% auto'  // Fill width, overflow height
            : 'auto 100%', // Fill height, overflow width
          opacity: imageOpacity
        }}
      />
      
      {/* ASCII Art - matches hero image scaling */}
      <div 
        className="absolute inset-0 w-full h-full flex items-center justify-center transition-opacity duration-300 ease-out overflow-hidden"
        style={{ opacity: asciiOpacity }}
      >
        <pre 
          className="text-white font-mono select-none pointer-events-none whitespace-pre"
          style={{
            fontSize: `${fontSize}px`,
            lineHeight: '1.2',
            letterSpacing: '0'
          }}
        >
          {asciiArt}
        </pre>
      </div>
    </div>
  )
}