import type { Metadata } from "next"
import { AuthProvider } from "@/lib/providers/AuthProvider"
import { QueryProvider } from "@/lib/providers/QueryProvider"
import "./globals.css"

export const metadata: Metadata = {
  title: "Event Aggregator",
  description: "University events platform",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-white text-slate-900 antialiased">
        <QueryProvider>
          <AuthProvider>
            {children}
          </AuthProvider>
        </QueryProvider>
      </body>
    </html>
  )
}
