import React, { useState, useEffect } from "react"
import { cn } from "@/lib/utils"

interface SillyLittleTestProps {
  title?: string
  count?: number
  onCountChange?: (newCount: number) => void
  className?: string
}

const SillyLittleTest: React.FC<SillyLittleTestProps> = ({
  title = "Silly Little Test Component",
  count = 0,
  onCountChange,
  className
}) => {
  const [internalCount, setInternalCount] = useState(count)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    setInternalCount(count)
  }, [count])

  const handleIncrement = async () => {
    setIsLoading(true)
    try {
      const newCount = internalCount + 1
      setInternalCount(newCount)
      onCountChange?.(newCount)
    } catch (error) {
      console.error("Failed to increment:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setInternalCount(0)
    onCountChange?.(0)
  }

  return (
    <div className={cn("p-6 border rounded-lg shadow-sm", className)}>
      <h2 className="text-xl font-bold mb-4">{title}</h2>
      <div className="flex items-center gap-4">
        <span className="text-2xl font-mono">{internalCount}</span>
        <button
          onClick={handleIncrement}
          disabled={isLoading}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {isLoading ? "Loading..." : "Increment"}
        </button>
        <button
          onClick={handleReset}
          className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
        >
          Reset
        </button>
      </div>
    </div>
  )
}

export default SillyLittleTest