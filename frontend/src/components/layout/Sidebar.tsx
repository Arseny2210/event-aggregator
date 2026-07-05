"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { motion, AnimatePresence } from "framer-motion"
import { cn } from "@/utils/cn"
import { useUIStore } from "@/lib/store/ui"
import {
  Bell,
  GraduationCap,
  Home,
  LayoutDashboard,
  Menu,
  Upload,
  X,
} from "lucide-react"

const navItems = [
  { href: "/dashboard", label: "Главная", icon: Home },
  { href: "/dashboard/events", label: "Мероприятия", icon: LayoutDashboard },
  { href: "/dashboard/imports", label: "Импорт", icon: Upload },
  { href: "/dashboard/notifications", label: "Уведомления", icon: Bell },
]

export function Sidebar() {
  const pathname = usePathname()
  const { sidebarOpen, toggleSidebar, closeSidebar } = useUIStore()

  return (
    <>
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={toggleSidebar}
        className="fixed left-4 top-4 z-50 rounded-xl border border-border bg-white p-2 shadow-sm lg:hidden"
        aria-label="Открыть меню"
      >
        {sidebarOpen ? (
          <X className="h-5 w-5 text-foreground" />
        ) : (
          <Menu className="h-5 w-5 text-foreground" />
        )}
      </motion.button>

      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-30 bg-black/30 backdrop-blur-sm lg:hidden"
            onClick={closeSidebar}
          />
        )}
      </AnimatePresence>

      <aside
        className={cn(
          "fixed left-0 top-0 z-40 h-full w-64 transform border-r border-border bg-white transition-transform duration-300 lg:relative lg:translate-x-0",
          sidebarOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="flex h-16 items-center gap-2 border-b border-border px-6">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-600 text-white">
            <GraduationCap className="h-5 w-5" />
          </div>
          <Link href="/dashboard" className="text-lg font-bold text-foreground">
            ИС «Мероприятия»
          </Link>
        </div>

        <nav className="mt-4 space-y-1 px-3">
          {navItems.map((item) => {
            const isActive =
              pathname === item.href ||
              (item.href !== "/dashboard" && pathname.startsWith(item.href))
            const Icon = item.icon
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={closeSidebar}
                className={cn(
                  "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all",
                  isActive
                    ? "bg-primary-50 text-primary-700"
                    : "text-foreground-secondary hover:bg-surface-tertiary hover:text-foreground",
                )}
              >
                <Icon className="h-4 w-4" />
                {item.label}
              </Link>
            )
          })}
        </nav>
      </aside>
    </>
  )
}
