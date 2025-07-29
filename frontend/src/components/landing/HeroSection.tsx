import TypingAnimation from './TypingAnimation'
import { ChevronDown } from "lucide-react"
import { useState, useEffect } from 'react'

export default function HeroSection() {
  const [showArrow, setShowArrow] = useState(false)
  const [ctaShown, setCTAShown] = useState(false)

  // Listen for CTA visibility from TypingAnimation
  useEffect(() => {
    // CTA show logic handled by parent component
  }, [])

  // Hide arrow on scroll
  useEffect(() => {
    const handleScroll = () => {
      if (ctaShown) {
        setShowArrow(window.scrollY <= 50)
      }
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [ctaShown])

  return (
    <section className="relative h-screen w-full bg-neutral-950/0 flex items-center justify-center mt-8">
      <TypingAnimation onCTAShow={() => { setCTAShown(true); setShowArrow(true); }} />
      
      {/* Animated Down Arrow - Bottom of section */}
      <div className={`absolute bottom-8 left-1/2 transform -translate-x-1/2 transition-all duration-1000 ${
        showArrow ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
      }`}>
        <ChevronDown 
          className="w-8 h-8 sm:w-12 sm:h-12 md:w-16 md:h-16 lg:w-20 lg:h-20 text-white/60 animate-bounce"
        />
      </div>
    </section>
  )
}