export default function RoadmapSection() {
  const roadmapItems = [
    {
      number: "00",
      title: "strong Agent compliance",
      description: "Agents document their reasoning and link every change back to your specs. Full accountability, no drift."
    },
    {
      number: "01", 
      title: "dynamic context management",
      description: "Smart context injection keeps agents laser-focused. They see only what matters for the task at hand."
    },
    {
      number: "02",
      title: "crystalized intention",
      description: "Turn natural conversations into complete specs. Cogent captures everything and builds a hierarchical spec tree."
    },
    {
      number: "03",
      title: "fully automatic and valid code",
      description: "With cogent any change to your linguistic object are implemented and validated automatically."
    },
    {
      number: "100",
      title: "The world of forms",
      description: "Ideas become reality seamlessly. The barrier between thought and creation dissolves."
    }
  ]

  return (
    <section className="w-full bg-neutral-950/90 border border-white/20 py-20">
      <div className="w-full">
        <div className="text-center mb-4">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-8" style={{ fontFamily: 'Kode Mono, monospace' }}>
            Roadmap
          </h2>
          <div className="flex justify-center">
            <span className="text-2xl font-bold" style={{ color: '#ECCD8C', fontFamily: 'Kode Mono, monospace' }}>init</span>
          </div>
        </div>
        
        <div className="max-w-4xl mx-auto relative">
          {/* Central vertical line */}
          <div className="absolute left-8 sm:left-1/2 sm:transform sm:-translate-x-px w-0.5 h-full bg-gray-500 opacity-50"></div>
          
          {roadmapItems.map((item, index) => (
            <div key={item.number} className="relative mb-16 sm:mb-20">
              {/* Circle at timeline point */}
              <div className="absolute left-8 sm:left-1/2 sm:transform sm:-translate-x-1/2 transform -translate-x-1/2 top-4">
                <div className="w-3 h-3 sm:w-4 sm:h-4 border-2 border-gray-500 rounded-full bg-transparent"></div>
              </div>
              
              {/* Roadmap item */}
              <div className={`relative flex ${index % 2 === 0 ? 'justify-start' : 'sm:justify-end justify-start'}`}>
                <div className={`w-full sm:w-5/12 pl-16 sm:pl-0 text-left ${index % 2 === 0 ? 'sm:pr-12 sm:text-right' : 'sm:pl-12 sm:text-left'}`}>
                  <div className="space-y-2 sm:space-y-3">
                    <div className={`flex items-center gap-2 sm:gap-3 justify-start ${index % 2 === 0 ? 'sm:justify-end' : 'sm:justify-start'}`}>
                      <span className="text-lg sm:text-2xl font-bold" style={{ color: '#ECCD8C', fontFamily: 'Kode Mono, monospace' }}>{item.number}.</span>
                      <h3 className="text-lg sm:text-xl lg:text-2xl font-bold" style={{ color: '#ECCD8C', fontFamily: 'Kode Mono, monospace' }}>
                        {item.title}
                      </h3>
                    </div>
                    <div className="w-full h-px bg-white/20"></div>
                    <p className="text-xs sm:text-sm lg:text-base text-white/90 leading-relaxed" style={{ fontFamily: 'Manrope, sans-serif' }}>
                      {item.description}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}