import { cn } from "@/utils/cn"
import { Button } from "@/components/ui/Button"

interface PaginationProps {
  offset: number
  limit: number
  total: number
  onPrevious: () => void
  onNext: () => void
}

export function Pagination({ offset, limit, total, onPrevious, onNext }: PaginationProps) {
  const from = total === 0 ? 0 : offset + 1
  const to = Math.min(offset + limit, total)
  const hasPrevious = offset > 0
  const hasNext = offset + limit < total

  return (
    <div className="flex items-center justify-between">
      <p className="text-sm text-slate-600">
        {total === 0 ? "No results" : `Showing ${from}-${to} of ${total}`}
      </p>
      <div className="flex gap-2">
        <Button variant="secondary" size="sm" onClick={onPrevious} disabled={!hasPrevious}>
          Previous
        </Button>
        <Button variant="secondary" size="sm" onClick={onNext} disabled={!hasNext}>
          Next
        </Button>
      </div>
    </div>
  )
}
