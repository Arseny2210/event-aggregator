"use client"

import { useAuth } from "@/lib/hooks/useAuth"
import { Button } from "@/components/ui/Button"
import { Avatar } from "@/components/ui/Avatar"
import { LogOut } from "lucide-react"

export function DashboardHeader() {
  const { user, logout } = useAuth()

  return (
    <header className="glass-strong sticky top-0 z-30 flex items-center justify-end gap-3 border-b border-border px-6 py-3">
      {user && (
        <div className="flex items-center gap-3">
          <div className="text-right">
            <p className="text-sm font-medium text-foreground">
              {user.email}
            </p>
            <p className="text-xs text-foreground-muted">
              {(user as { role?: { name: string } }).role?.name === "administrator" ? "Администратор" : "Редактор"}
            </p>
          </div>
          <Avatar name={user.email} size="md" />
        </div>
      )}
      <Button variant="ghost" size="sm" onClick={logout}>
        <LogOut className="mr-1.5 h-4 w-4" />
        Выйти
      </Button>
    </header>
  )
}
