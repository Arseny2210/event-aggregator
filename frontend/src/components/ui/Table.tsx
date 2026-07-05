import { cn } from "@/utils/cn"

interface TableProps {
  children: React.ReactNode
  className?: string
}

export function Table({ children, className }: TableProps) {
  return (
    <div className="overflow-x-auto rounded-xl border border-border bg-white shadow-sm">
      <table className={cn("w-full text-left text-sm", className)}>
        {children}
      </table>
    </div>
  )
}

export function TableHead({ children, className }: TableProps) {
  return (
    <thead className={cn("border-b border-border bg-surface-secondary", className)}>
      {children}
    </thead>
  )
}

export function TableBody({ children, className }: TableProps) {
  return (
    <tbody className={cn("divide-y divide-border", className)}>
      {children}
    </tbody>
  )
}

export function TableRow({ children, className }: TableProps) {
  return (
    <tr className={cn("transition-colors hover:bg-surface-secondary", className)}>
      {children}
    </tr>
  )
}

export function TableHeader({ children, className }: TableProps) {
  return (
    <th className={cn("px-4 py-3 text-xs font-semibold uppercase tracking-wider text-foreground-secondary", className)}>
      {children}
    </th>
  )
}

export function TableCell({ children, className }: TableProps) {
  return (
    <td className={cn("px-4 py-3 text-foreground", className)}>
      {children}
    </td>
  )
}
