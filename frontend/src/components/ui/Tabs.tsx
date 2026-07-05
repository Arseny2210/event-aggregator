"use client"

import { motion } from "framer-motion"
import { cn } from "@/utils/cn"

interface Tab {
  id: string
  label: string
}

interface TabsProps {
  tabs: Tab[]
  activeTab: string
  onTabChange: (id: string) => void
  className?: string
}

export function Tabs({ tabs, activeTab, onTabChange, className }: TabsProps) {
  return (
    <div className={cn("flex gap-1 rounded-xl bg-surface-tertiary p-1", className)}>
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          className={cn(
            "relative rounded-lg px-4 py-2 text-sm font-medium transition-colors",
            activeTab === tab.id
              ? "text-foreground"
              : "text-foreground-muted hover:text-foreground-secondary",
          )}
        >
          {activeTab === tab.id && (
            <motion.div
              layoutId="activeTab"
              className="absolute inset-0 rounded-lg bg-white shadow-sm"
              transition={{ type: "spring", duration: 0.3 }}
            />
          )}
          <span className="relative z-10">{tab.label}</span>
        </button>
      ))}
    </div>
  )
}
