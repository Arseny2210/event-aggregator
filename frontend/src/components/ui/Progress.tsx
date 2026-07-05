"use client"

import { cn } from "@/utils/cn"
import { motion } from "framer-motion"

interface ProgressProps {
  value: number
  className?: string
}

export function Progress({ value, className }: ProgressProps) {
  const pct = Math.min(100, Math.max(0, value))
  const color =
    pct >= 100 ? "bg-green-500" : pct >= 50 ? "bg-amber-500" : "bg-primary-500"

  return (
    <div className={cn("h-2 w-full overflow-hidden rounded-full bg-surface-tertiary", className)}>
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: `${pct}%` }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className={cn("h-full rounded-full", color)}
        role="progressbar"
        aria-valuenow={pct}
        aria-valuemin={0}
        aria-valuemax={100}
      />
    </div>
  )
}
