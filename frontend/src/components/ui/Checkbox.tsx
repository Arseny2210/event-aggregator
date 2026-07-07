"use client"

import { forwardRef } from "react"
import { cn } from "@/utils/cn"

interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "type"> {
  label?: string
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ className, label, id, ...props }, ref) => {
    return (
      <label className="inline-flex cursor-pointer items-center gap-2">
        <input
          ref={ref}
          type="checkbox"
          id={id}
          className={cn(
            "h-4 w-4 rounded border-border text-primary-600 focus:ring-2 focus:ring-primary-500",
            className,
          )}
          {...props}
        />
        {label && <span className="text-sm text-foreground">{label}</span>}
      </label>
    )
  },
)

Checkbox.displayName = "Checkbox"
