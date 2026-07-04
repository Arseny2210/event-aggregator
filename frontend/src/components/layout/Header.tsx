"use client"

import Link from "next/link"
import { useAuth } from "@/lib/hooks/useAuth"
import { Button } from "@/components/ui/Button"

export function Header() {
  const { isAuthenticated, user, logout } = useAuth()

  return (
    <header className="border-b border-slate-200">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <Link href="/" className="text-lg font-bold text-slate-900">
          Event Aggregator
        </Link>
        <div className="flex items-center gap-4 text-sm font-medium">
          {isAuthenticated ? (
            <>
              <span className="text-slate-600">{user?.email}</span>
              <Link href="/dashboard">
                <Button variant="ghost" size="sm">Dashboard</Button>
              </Link>
              <Button variant="ghost" size="sm" onClick={logout}>
                Sign Out
              </Button>
            </>
          ) : (
            <Link href="/login" className="text-slate-600 hover:text-slate-900">
              Sign In
            </Link>
          )}
        </div>
      </nav>
    </header>
  )
}
