import { useEffect, useRef, useState } from 'react'

export default function IntroSection() {
  const [isVisible, setIsVisible] = useState(false);
  const sectionRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(true)
          }
        })
      },
      { threshold: 0.1 }
    )

    if (sectionRef.current) {
      observer.observe(sectionRef.current)
    }

    return () => {
      if (sectionRef.current) {
        observer.unobserve(sectionRef.current)
      }
    }
  }, [])

  return (
    <section 
      id="intro"
      ref={sectionRef}
      className={`w-full bg-neutral-950/75 border border-white/20 py-8 transition-all duration-1000 relative overflow-hidden ${
        isVisible 
          ? 'opacity-100 translate-y-0' 
          : 'opacity-0 translate-y-10'
      }`}
    >
      {/* Cogent Sun Logo - Top Right Quarter */}
      <div className="absolute -top-48 -right-48 w-96 h-96 opacity-50 pointer-events-none">
        <img 
          src="/cogent-sun-logo.svg" 
          alt="" 
          className="w-full h-full object-contain"
        />
      </div>
      
      <div className="w-full text-white px-8 relative z-10">
        <h2 className="text-4xl font-bold mb-32 text-left max-w-xl" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
          <span className="text-yellow-400">Production-ready</span> full-stack apps built from plaintext specification trees
        </h2>
        <h3 className="text-3xl font-bold text-right max-w-xl ml-auto" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
          Cogent interviews you about your idea and collaboratively constructs the spec tree with you.
        </h3>
      </div>
    </section>
  )
}
