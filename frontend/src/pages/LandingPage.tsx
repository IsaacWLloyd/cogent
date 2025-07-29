import StickyWallpaper from '../components/landing/StickyWallpaper'
import Navbar from '../components/landing/Navbar'
import HeroSection from '../components/landing/HeroSection'
import QuickPitchSection from '../components/landing/QuickPitchSection'
import VisualExplainerSection from '../components/landing/VisualExplainerSection'
import RoadmapSection from '../components/landing/RoadmapSection'
import FinalSection from '../components/landing/FinalSection'
import PageWrapper from '../components/landing/PageWrapper'

interface LandingPageProps {
  onOpenTerminal: () => void
}

export default function LandingPage({ onOpenTerminal }: LandingPageProps) {
  return (
    <main className="relative bg-black">
      <Navbar onOpenTerminal={onOpenTerminal} />
      <StickyWallpaper />
      
      <div className="relative z-20">
        <HeroSection />
        
        <PageWrapper>
          <QuickPitchSection />
        </PageWrapper>
        
        <PageWrapper>
          <VisualExplainerSection />
        </PageWrapper>
        
        <PageWrapper>
          <RoadmapSection />
        </PageWrapper>
        
        <PageWrapper>
          <FinalSection />
        </PageWrapper>
      </div>
    </main>
  )
}