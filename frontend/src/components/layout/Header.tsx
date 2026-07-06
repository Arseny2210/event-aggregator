"use client"

import Link from "next/link"
import { GraduationCap } from "lucide-react"

export function Header() {
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
      </nav>
    </header>
  )
}
