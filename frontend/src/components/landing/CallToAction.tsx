import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface CallToActionProps {
  isVisible: boolean
}

export default function CallToAction({ isVisible }: CallToActionProps) {
  const [email, setEmail] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [message, setMessage] = useState("")
  const [isSuccess, setIsSuccess] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setMessage("")
    
    try {
      const response = await fetch('/api/v1/waitlist', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      })
      
      const data = await response.json()
      
      if (data.success) {
        setIsSuccess(true)
        setMessage(data.message)
        setEmail("")
      } else {
        setIsSuccess(false)
        setMessage(data.message || "Failed to join waitlist")
      }
    } catch (error) {
      setIsSuccess(false)
      setMessage("Failed to join waitlist")
      console.error("Waitlist signup error:", error)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className={`flex flex-col items-center space-y-3 sm:space-y-4 pt-4 transition-all duration-500 ${
      isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
    }`}>
      {/* Waitlist Card */}
      <Card className="w-56 sm:w-64 lg:w-72 bg-neutral-950 border border-white/20 rounded-sm">
        <CardHeader className="pb-4">
          <CardTitle className="text-white text-center text-xl font-display">Join us.</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="bg-neutral-800/50 border-white/20 text-white placeholder:text-neutral-400 rounded-sm focus:border-white/40"
              required
              disabled={isSubmitting}
            />
            <Button 
              type="submit" 
              className="w-full bg-white text-neutral-950 hover:bg-neutral-100 rounded-sm font-medium disabled:opacity-50"
              disabled={isSubmitting}
            >
              {isSubmitting ? "Joining..." : "Join Waitlist"}
            </Button>
            {message && (
              <p className={`text-sm text-center ${isSuccess ? 'text-green-400' : 'text-red-400'}`}>
                {message}
              </p>
            )}
          </form>
        </CardContent>
      </Card>

      {/* Discord Placeholder Box */}
      <div className="w-56 sm:w-64 lg:w-72 h-16 sm:h-18 bg-neutral-950 border border-white/20 rounded-sm flex items-center justify-center">
        <span className="text-neutral-400 text-sm">Discord embed will go here</span>
      </div>

    </div>
  )
}