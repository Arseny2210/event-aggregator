"use client"

import { motion } from "framer-motion"
import { cn } from "@/utils/cn"
import type { LucideIcon } from "lucide-react"

interface DashboardCardProps {
  title: string
  value: string | number
  description?: string
  icon: LucideIcon
  color?: "blue" | "green" | "amber" | "purple"
  className?: string
}

const colorConfig = {
  blue: {
    bg: "bg-blue-50",
    text: "text-blue-600",
    icon: "text-blue-600",
  },
  green: {
    bg: "bg-green-50",
    text: "text-green-600",
    icon: "text-green-600",
  },
  amber: {
    bg: "bg-amber-50",
    text: "text-amber-600",
    icon: "text-amber-600",
  },
  purple: {
    bg: "bg-purple-50",
    text: "text-purple-600",
    icon: "text-purple-600",
  },
}

export function DashboardCard({
  title,
  value,
  description,
  icon: Icon,
  color = "blue",
  className,
}: DashboardCardProps) {
  const colors = colorConfig[color]

  return (
    <motion.div
      whileHover={{ y: -2 }}
      className={cn(
        "rounded-2xl border border-border bg-white p-6 shadow-card transition-shadow hover:shadow-card-hover",
        className,
      )}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-foreground-secondary">
            {title}
          </p>
          <p className="mt-1 text-3xl font-bold text-foreground">{value}</p>
          {description && (
            <p className="mt-1 text-xs text-foreground-muted">{description}</p>
          )}
        </div>
        <div className={cn("flex h-10 w-10 items-center justify-center rounded-xl", colors.bg)}>
          <Icon className={cn("h-5 w-5", colors.icon)} />
        </div>
      </div>
    </motion.div>
  )
}
