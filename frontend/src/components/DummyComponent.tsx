import * as React from "react"

interface DummyComponentProps {
  placeholder?: string
}

const DummyComponent: React.FC<DummyComponentProps> = ({ placeholder = "Dummy Component" }) => {
  return (
    <div className="p-4 border border-dashed border-gray-300 rounded-md">
      <p className="text-gray-500">{placeholder}</p>
    </div>
  )
}

export default DummyComponent