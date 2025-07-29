import { ReactNode } from 'react'

interface PageWrapperProps {
  children: ReactNode
  className?: string
}

export default function PageWrapper({ children, className = '' }: PageWrapperProps) {
  return (
    <div className={`w-full lg:max-w-6xl lg:mx-auto lg:px-8 px-4 sm:px-6 ${className}`}>
      {children}
    </div>
  )
}