"use client"

import { useAuth } from "@/lib/hooks/useAuth"
import { useUIStore } from "@/lib/store/ui"
import { Button } from "@/components/ui/Button"
import { Menu, LogOut } from "lucide-react"

export function DashboardHeader() {
  const { user, logout } = useAuth()
  const { toggleSidebar } = useUIStore()

  return (
    <header className="glass-strong flex h-16 items-center justify-between border-b border-border px-4 lg:px-8">
      <button
        onClick={toggleSidebar}
        className="rounded-xl p-2 text-foreground-secondary hover:bg-surface-tertiary lg:hidden"
        aria-label="Открыть меню"
      >
        <Menu className="h-5 w-5" />
      </button>

      <div className="ml-auto flex items-center gap-4">
        <span className="text-sm text-foreground-secondary">{user?.email}</span>
        <Button variant="ghost" size="sm" onClick={logout}>
          <LogOut className="mr-2 h-4 w-4" />
          Выйти
        </Button>
      </div>
    </header>
  )
}
