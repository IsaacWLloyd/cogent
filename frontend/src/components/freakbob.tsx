import * as React from "react"

interface FreakbobProps {
  placeholder?: string
}

const Freakbob: React.FC<FreakbobProps> = ({ placeholder = "Freakbob Component" }) => {
  return (
    <div className="p-4 border border-dashed border-gray-300 rounded-md">
      <p className="text-gray-500">{placeholder}</p>
    </div>
  )
}

export default Freakbob