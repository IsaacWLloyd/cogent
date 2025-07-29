import React, { useState } from "react"
import { Button } from "@/components/ui/button"

interface FinalTestProps {
  initialValue?: number
  onUpdate?: (value: number) => void
}

const FinalTest: React.FC<FinalTestProps> = ({ 
  initialValue = 0, 
  onUpdate 
}) => {
  const [value, setValue] = useState(initialValue)

  const handleIncrement = () => {
    const newValue = value + 1
    setValue(newValue)
    onUpdate?.(newValue)
  }

  return (
    <div className="flex items-center gap-4 p-4">
      <span className="text-lg">Value: {value}</span>
      <Button onClick={handleIncrement}>
        Increment
      </Button>
    </div>
  )
}

export default FinalTest