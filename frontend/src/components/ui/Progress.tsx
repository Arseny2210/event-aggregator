import { cn } from "@/utils/cn"

interface ProgressProps {
  value: number
  className?: string
}

export function Progress({ value, className }: ProgressProps) {
  const pct = Math.min(100, Math.max(0, value))
  const color =
    pct >= 100 ? "bg-green-500" : pct >= 50 ? "bg-amber-500" : "bg-blue-500"

  return (
    <div className={cn("h-2 w-full overflow-hidden rounded-full bg-slate-200", className)}>
      <div
        className={cn("h-full rounded-full transition-all duration-500", color)}
        style={{ width: `${pct}%` }}
        role="progressbar"
        aria-valuenow={pct}
        aria-valuemin={0}
        aria-valuemax={100}
      />
    </div>
  )
}
