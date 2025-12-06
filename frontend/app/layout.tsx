import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'JobPortal - AI-Powered Job Matching',
  description: 'Find your perfect job or candidate with AI-powered matching',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="font-sans">{children}</body>
    </html>
  )
}
