import { Routes, Route } from 'react-router-dom'
import { useState } from 'react'
import LandingPage from './pages/LandingPage'
import TerminalModal from './components/landing/TerminalModal'

function App() {
  const [showTerminalModal, setShowTerminalModal] = useState(false)

  return (
    <div className="dark min-h-screen bg-black text-white">
      <Routes>
        <Route path="/" element={<LandingPage onOpenTerminal={() => setShowTerminalModal(true)} />} />
        {/* Catch all route - redirect to home */}
        <Route path="*" element={<LandingPage onOpenTerminal={() => setShowTerminalModal(true)} />} />
      </Routes>
      
      {/* Terminal Modal */}
      <TerminalModal 
        isOpen={showTerminalModal}
        onClose={() => setShowTerminalModal(false)}
      />
    </div>
  )
}

export default App