import React from "react"

interface AutoDocTestProps {
  message: string
}

const AutoDocTest: React.FC<AutoDocTestProps> = ({ message }) => {
  return (
    <div className="p-4 bg-gray-100 rounded">
      <h3 className="font-bold">Auto Documentation Test</h3>
      <p>{message}</p>
    </div>
  )
}

export default AutoDocTest