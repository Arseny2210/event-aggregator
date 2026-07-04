import { cn } from "@/utils/cn"
import { AlertCircle, CheckCircle, Info } from "lucide-react"

const variants = {
  error: "border-red-200 bg-red-50 text-red-800",
  success: "border-green-200 bg-green-50 text-green-800",
  info: "border-blue-200 bg-blue-50 text-blue-800",
} as const

const icons = {
  error: AlertCircle,
  success: CheckCircle,
  info: Info,
} as const

interface AlertProps {
  variant?: keyof typeof variants
  children: React.ReactNode
  className?: string
}

export function Alert({ variant = "info", children, className }: AlertProps) {
  const Icon = icons[variant]
  return (
    <div className={cn("flex items-start gap-3 rounded-lg border p-4 text-sm", variants[variant], className)}>
      <Icon className="mt-0.5 h-4 w-4 flex-shrink-0" />
      <span>{children}</span>
    </div>
  )
}
