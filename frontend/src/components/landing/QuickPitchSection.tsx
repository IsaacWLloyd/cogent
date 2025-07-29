import { useEffect, useRef, useState } from 'react'

export default function QuickPitchSection() {
  const [visibleElements, setVisibleElements] = useState(new Set())
  const divsRef = useRef<(HTMLDivElement | null)[]>([])

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setVisibleElements((prev) => new Set(prev).add(entry.target.id))
          }
        })
      },
      { threshold: 0.1 }
    )

    divsRef.current.forEach((div) => {
      if (div) observer.observe(div)
    })

    return () => {
      divsRef.current.forEach((div) => {
        if (div) observer.unobserve(div)
      })
    }
  }, [])

  return (
    <section id="quick-pitch" className="w-full bg-neutral-950/50 border border-white/20 py-20 flex items-center">
      <div className="w-full">
        <div className="flex flex-col space-y-12">
          {/* Diagram 1 */}
          <div 
            ref={(el) => (divsRef.current[0] = el)}
            id="diagram1"
            className={`w-full border-2 border-[#ECCD8C] transition-all duration-1000 ${
              visibleElements.has('diagram1') 
                ? 'opacity-100 translate-y-0' 
                : 'opacity-0 translate-y-10'
            }`}
          >
            <img 
              src="/diagram1.svg" 
              alt="Diagram 1" 
              className="w-full h-auto"
            />
          </div>
          
          {/* Copy 1 */}
          <div 
            ref={(el) => (divsRef.current[1] = el)}
            id="copy1"
            className={`text-white px-8 py-12 text-center transition-all duration-1000 delay-200 bg-white/5 backdrop-blur-[30%] ${
              visibleElements.has('copy1')
                ? 'opacity-100 translate-y-0'
                : 'opacity-0 translate-y-10'
            }`}
          >
            <h3 className="text-3xl font-bold mb-6" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              Coding agents don't go all the way
            </h3>
            <p className="text-lg leading-relaxed max-w-4xl mx-auto" style={{ fontFamily: 'Manrope, sans-serif' }}>
              Current coding agents write lots of code fast but they miss what matters. tools like cursor or Claude Code lose context, drift from specifications, and fail to implement your precise and glorious vision. What's worse, the prompts we use to control them are hard to iterate on and even harder to keep track of.
            </p>
          </div>
          
          {/* Diagram 2 */}
          <div 
            ref={(el) => (divsRef.current[2] = el)}
            id="diagram2"
            className={`w-full border-2 border-[#ECCD8C] transition-all duration-1000 ${
              visibleElements.has('diagram2')
                ? 'opacity-100 translate-y-0'
                : 'opacity-0 translate-y-10'
            }`}
          >
            <img 
              src="/diagram2.svg" 
              alt="Diagram 2" 
              className="w-full h-auto"
            />
          </div>
          
          {/* Copy 2 */}
          <div 
            ref={(el) => (divsRef.current[3] = el)}
            id="copy2"
            className={`text-white px-8 py-12 text-center transition-all duration-1000 delay-200 bg-white/5 backdrop-blur-[30%] ${
              visibleElements.has('copy2')
                ? 'opacity-100 translate-y-0'
                : 'opacity-0 translate-y-10'
            }`}
          >
            <h3 className="text-3xl font-bold mb-6" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              Cogent bridges the gap
            </h3>
            <p className="text-lg leading-relaxed max-w-4xl mx-auto" style={{ fontFamily: 'Manrope, sans-serif' }}>
	      Finally, coding agents that stay on target. Cogent forces agents to document all their changes - both granular and high-level - while feeding them just the right context at each step. We translate your vision into clear specifications through conversation, then keep agents locked onto them.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
