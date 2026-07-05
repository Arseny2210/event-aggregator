"use client"

import Link from "next/link"
import { useAuth } from "@/lib/hooks/useAuth"
import { Button } from "@/components/ui/Button"
import { GraduationCap, LogOut, LayoutDashboard } from "lucide-react"

export function Header() {
  const { isAuthenticated, user, logout } = useAuth()

  return (
    <header className="glass sticky top-0 z-40 border-b border-border">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link href="/" className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-600 text-white">
            <GraduationCap className="h-5 w-5" />
          </div>
          <span className="text-lg font-bold text-foreground">
            ИС «Мероприятия»
          </span>
        </Link>
        <div className="flex items-center gap-3 text-sm font-medium">
          {isAuthenticated ? (
            <>
              <span className="text-foreground-secondary">{user?.email}</span>
              <Link href="/dashboard">
                <Button variant="ghost" size="sm">
                  <LayoutDashboard className="mr-1.5 h-4 w-4" />
                  Панель
                </Button>
              </Link>
              <Button variant="ghost" size="sm" onClick={logout}>
                <LogOut className="mr-1.5 h-4 w-4" />
                Выйти
              </Button>
            </>
          ) : (
            <Link href="/login">
              <Button variant="ghost" size="sm">
                Войти
              </Button>
            </Link>
          )}
        </div>
      </nav>
    </header>
  )
}
