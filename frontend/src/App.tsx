import { Routes, Route } from 'react-router-dom'
import Navbar from './components/layout/Navbar'
import LandingPage from './pages/LandingPage'

function App() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        {/* Add more routes here later */}
      </Routes>
    </div>
  )
}

export default App