import { cn } from "@/utils/cn"

interface TableProps {
  children: React.ReactNode
  className?: string
}

export function Table({ children, className }: TableProps) {
  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200">
      <table className={cn("w-full text-left text-sm", className)}>{children}</table>
    </div>
  )
}

export function TableHead({ children, className }: TableProps) {
  return <thead className={cn("border-b border-slate-200 bg-slate-50", className)}>{children}</thead>
}

export function TableBody({ children, className }: TableProps) {
  return <tbody className={cn("divide-y divide-slate-200", className)}>{children}</tbody>
}

export function TableRow({ children, className }: TableProps) {
  return <tr className={cn("hover:bg-slate-50", className)}>{children}</tr>
}

export function TableHeader({ children, className }: TableProps) {
  return <th className={cn("px-4 py-3 font-medium text-slate-600", className)}>{children}</th>
}

export function TableCell({ children, className }: TableProps) {
  return <td className={cn("px-4 py-3 text-slate-900", className)}>{children}</td>
}
