"use client"

import { useAuth } from "@/lib/hooks/useAuth"
import { useUIStore } from "@/lib/store/ui"
import { Button } from "@/components/ui/Button"
import { Menu, LogOut } from "lucide-react"

export function DashboardHeader() {
  const { user, logout } = useAuth()
  const { toggleSidebar } = useUIStore()

  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-200 px-4 lg:px-8">
      <button
        onClick={toggleSidebar}
        className="rounded-lg p-2 text-slate-600 hover:bg-slate-100 lg:hidden"
        aria-label="Toggle sidebar"
      >
        <Menu className="h-5 w-5" />
      </button>

      <div className="flex items-center gap-4 ml-auto">
        <span className="text-sm text-slate-600">
          {user?.email}
        </span>
        <Button variant="ghost" size="sm" onClick={logout}>
          <LogOut className="mr-2 h-4 w-4" />
          Sign Out
        </Button>
      </div>
    </header>
  )
}
