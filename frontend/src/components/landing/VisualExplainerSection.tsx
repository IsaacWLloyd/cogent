export default function VisualExplainerSection() {
  return (
    <section className="w-full bg-neutral-950/75 border border-white/20 py-20">
      <div className="w-full">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Step 1 */}
          <div className="bg-black/50 p-8 space-y-6">
            <div>
              <h3 className="text-2xl font-bold" style={{ color: '#ECCD8C', fontFamily: 'Kode Mono, monospace' }}>
                cogent picks your brain
              </h3>
              <p className="text-white/90 mt-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                Cogent chats with you in a branching chat flow, exploring all angles of your project.
              </p>
            </div>
            {/* Chat bubbles placeholder */}
            <div className="flex flex-col space-y-3 mt-8">
              <div className="w-3/4 h-12 bg-white/20 rounded-lg self-start"></div>
              <div className="w-2/3 h-12 bg-white/20 rounded-lg self-end"></div>
              <div className="w-3/4 h-12 bg-white/20 rounded-lg self-start"></div>
            </div>
          </div>

          {/* Step 2 */}
          <div className="bg-black/50 p-8 space-y-6">
            <div>
              <h3 className="text-2xl font-bold" style={{ color: '#ECCD8C', fontFamily: 'Kode Mono, monospace' }}>
                cogent crystallizes your intent
              </h3>
              <p className="text-white/90 mt-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                Cogent uses broad and specific insights from your conversation to construct a hierarchical tree of specifications, design documents, and validation tests.
              </p>
            </div>
            {/* Hierarchical tree placeholder */}
            <div className="mt-8">
              <svg viewBox="0 0 300 200" className="w-full h-48">
                <line x1="150" y1="20" x2="75" y2="60" stroke="white" strokeWidth="2" opacity="0.3"/>
                <line x1="150" y1="20" x2="150" y2="60" stroke="white" strokeWidth="2" opacity="0.3"/>
                <line x1="150" y1="20" x2="225" y2="60" stroke="white" strokeWidth="2" opacity="0.3"/>
                <line x1="75" y1="60" x2="40" y2="100" stroke="white" strokeWidth="2" opacity="0.3"/>
                <line x1="75" y1="60" x2="110" y2="100" stroke="white" strokeWidth="2" opacity="0.3"/>
                <line x1="150" y1="60" x2="150" y2="100" stroke="white" strokeWidth="2" opacity="0.3"/>
                <line x1="225" y1="60" x2="190" y2="100" stroke="white" strokeWidth="2" opacity="0.3"/>
                <line x1="225" y1="60" x2="260" y2="100" stroke="white" strokeWidth="2" opacity="0.3"/>
                <line x1="40" y1="100" x2="20" y2="140" stroke="white" strokeWidth="2" opacity="0.3"/>
                <line x1="40" y1="100" x2="60" y2="140" stroke="white" strokeWidth="2" opacity="0.3"/>
                <line x1="110" y1="100" x2="110" y2="140" stroke="white" strokeWidth="2" opacity="0.3"/>
                <line x1="150" y1="100" x2="130" y2="140" stroke="white" strokeWidth="2" opacity="0.3"/>
                <line x1="150" y1="100" x2="170" y2="140" stroke="white" strokeWidth="2" opacity="0.3"/>
                <line x1="260" y1="100" x2="260" y2="140" stroke="white" strokeWidth="2" opacity="0.3"/>
                {/* Nodes */}
                <circle cx="150" cy="20" r="8" fill="white" opacity="0.5"/>
                <circle cx="75" cy="60" r="6" fill="white" opacity="0.5"/>
                <circle cx="150" cy="60" r="6" fill="white" opacity="0.5"/>
                <circle cx="225" cy="60" r="6" fill="white" opacity="0.5"/>
                <circle cx="40" cy="100" r="5" fill="white" opacity="0.5"/>
                <circle cx="110" cy="100" r="5" fill="white" opacity="0.5"/>
                <circle cx="150" cy="100" r="5" fill="white" opacity="0.5"/>
                <circle cx="190" cy="100" r="5" fill="white" opacity="0.5"/>
                <circle cx="260" cy="100" r="5" fill="white" opacity="0.5"/>
                <circle cx="20" cy="140" r="4" fill="white" opacity="0.5"/>
                <circle cx="60" cy="140" r="4" fill="white" opacity="0.5"/>
                <circle cx="110" cy="140" r="4" fill="white" opacity="0.5"/>
                <circle cx="130" cy="140" r="4" fill="white" opacity="0.5"/>
                <circle cx="170" cy="140" r="4" fill="white" opacity="0.5"/>
                <circle cx="260" cy="140" r="4" fill="white" opacity="0.5"/>
              </svg>
            </div>
          </div>

          {/* Step 3 */}
          <div className="bg-black/50 p-8 space-y-6">
            <div>
              <h3 className="text-2xl font-bold" style={{ color: '#ECCD8C', fontFamily: 'Kode Mono, monospace' }}>
                cogent manages your agents
              </h3>
              <p className="text-white/90 mt-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                Cogent keeps your agents accountable by requiring them to document every change and explain how it meets the relevant specifications. At the same time, it dynamically provides exactly the context they need at each step.
              </p>
            </div>
            {/* Cogent logo managing agents placeholder */}
            <div className="relative flex items-center justify-center mt-8">
              {/* Gray connecting lines */}
              <svg className="absolute w-full h-20" viewBox="0 0 300 80">
                <line x1="75" y1="40" x2="125" y2="40" stroke="gray" strokeWidth="2" opacity="0.5"/>
                <line x1="175" y1="40" x2="225" y2="40" stroke="gray" strokeWidth="2" opacity="0.5"/>
              </svg>
              
              {/* Content */}
              <div className="relative flex items-center space-x-12">
                {/* Left robot emoji */}
                <span className="text-4xl grayscale">🤖</span>
                
                {/* Cogent sun logo */}
                <img 
                  src="/cogent-sun-logo.svg" 
                  alt="Cogent" 
                  className="w-16 h-16"
                />
                
                {/* Right robot emoji */}
                <span className="text-4xl grayscale">🤖</span>
              </div>
            </div>
          </div>

          {/* Step 4 */}
          <div className="bg-black/50 p-8 space-y-6">
            <div>
              <h3 className="text-2xl font-bold" style={{ color: '#ECCD8C', fontFamily: 'Kode Mono, monospace' }}>
                cogent automatically validates and iterates
              </h3>
              <p className="text-white/90 mt-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                Using your testing specifications, Cogent ensures that the agents are passing tests, and if not, it forces them to fix it.
                <br /><br />
                When you update or add a specification, Cogent knows exactly what needs to change and can automatically deploy an agent to do so.
              </p>
            </div>
            {/* Test checklist placeholder */}
            <div className="space-y-3 mt-8" style={{ fontFamily: 'Kode Mono, monospace' }}>
              <div className="flex items-center space-x-3">
                <span className="text-white/50">[✓]</span>
                <div className="w-48 h-6 bg-white/10"></div>
              </div>
              <div className="flex items-center space-x-3">
                <span className="text-white/50">[✓]</span>
                <div className="w-56 h-6 bg-white/10"></div>
              </div>
              <div className="flex items-center space-x-3">
                <span className="text-white/50">[✗]</span>
                <div className="w-52 h-6 bg-white/10"></div>
              </div>
              <div className="flex items-center space-x-3">
                <span className="text-white/50">[✓]</span>
                <div className="w-44 h-6 bg-white/10"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
