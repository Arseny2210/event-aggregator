"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/utils/cn"
import { useUIStore } from "@/lib/store/ui"
import {
  BarChart3,
  Bell,
  Home,
  LayoutDashboard,
  Menu,
  Upload,
  Users,
  X,
} from "lucide-react"

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: Home },
  { href: "/dashboard/events", label: "Events", icon: LayoutDashboard },
  { href: "/dashboard/imports", label: "Imports", icon: Upload },
  { href: "/dashboard/notifications", label: "Notifications", icon: Bell },
  { href: "/dashboard/statistics", label: "Statistics", icon: BarChart3 },
  { href: "/dashboard/users", label: "Users", icon: Users },
]

export function Sidebar() {
  const pathname = usePathname()
  const { sidebarOpen, toggleSidebar, closeSidebar } = useUIStore()

  return (
    <>
      <button
        onClick={toggleSidebar}
        className="fixed left-4 top-4 z-50 rounded-lg border border-slate-200 bg-white p-2 lg:hidden"
        aria-label="Toggle sidebar"
      >
        {sidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
      </button>

      {sidebarOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/30 lg:hidden"
          onClick={closeSidebar}
        />
      )}

      <aside
        className={cn(
          "fixed left-0 top-0 z-40 h-full w-64 transform border-r border-slate-200 bg-white transition-transform duration-200 lg:relative lg:translate-x-0",
          sidebarOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="flex h-16 items-center border-b border-slate-200 px-6">
          <Link href="/dashboard" className="text-lg font-bold text-slate-900">
            Event Aggregator
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
                  "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-blue-50 text-blue-700"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-900",
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
