"use client"

import Link from "next/link"
import { Eye, Trash2, Upload } from "lucide-react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/Table"
import { Badge } from "@/components/ui/Badge"
import { Pagination } from "@/components/ui/Pagination"
import { Progress } from "@/components/ui/Progress"
import { Spinner } from "@/components/ui/Spinner"
import { Alert } from "@/components/ui/Alert"
import { Button } from "@/components/ui/Button"
import { Select } from "@/components/ui/Select"
import { useImports } from "@/lib/hooks/useImports"
import type { ImportStatus } from "@/types/imports"
import { IMPORT_STATUS_COLORS, IMPORT_STATUS_LABELS } from "@/types/imports"

interface ImportListProps {
  offset: number
  limit: number
  status: string
  onPageChange: (offset: number) => void
  onStatusChange: (status: string) => void
}

const STATUS_OPTIONS = [
  { value: "", label: "All statuses" },
  { value: "processing", label: "Processing" },
  { value: "completed", label: "Completed" },
  { value: "failed", label: "Failed" },
]

export function ImportList({ offset, limit, status, onPageChange, onStatusChange }: ImportListProps) {
  const params = {
    offset,
    limit,
    status: (status || undefined) as ImportStatus | undefined,
  }
  const { data, isLoading, error } = useImports(params)

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <div className="w-40">
          <Select
            options={STATUS_OPTIONS}
            value={status}
            onChange={(e) => {
              onStatusChange(e.target.value)
              onPageChange(0)
            }}
          />
        </div>
      </div>

      {isLoading && (
        <div className="flex items-center justify-center py-12">
          <Spinner className="h-8 w-8" />
        </div>
      )}

      {error && <Alert variant="error">Failed to load imports: {error.message}</Alert>}

      {data && data.items.length === 0 && (
        <div className="py-12 text-center">
          <Upload className="mx-auto mb-3 h-8 w-8 text-slate-400" />
          <p className="text-slate-500">No imports found.</p>
        </div>
      )}

      {data && data.items.length > 0 && (
        <Table>
          <TableHead>
            <TableRow>
              <TableHeader>Filename</TableHeader>
              <TableHeader>Status</TableHeader>
              <TableHeader>Progress</TableHeader>
              <TableHeader>Created</TableHeader>
              <TableHeader className="w-16">Actions</TableHeader>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.items.map((job) => (
              <TableRow key={job.id}>
                <TableCell className="font-medium">{job.filename}</TableCell>
                <TableCell>
                  <Badge className={IMPORT_STATUS_COLORS[job.status]}>
                    {IMPORT_STATUS_LABELS[job.status]}
                  </Badge>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <Progress value={job.summary.progress_percent} className="w-24" />
                    <span className="text-xs text-slate-500">
                      {job.summary.progress_percent}%
                    </span>
                  </div>
                </TableCell>
                <TableCell className="text-slate-500">
                  {new Date(job.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  <Link href={`/dashboard/imports/${job.id}`}>
                    <Button variant="ghost" size="sm" aria-label="View import">
                      <Eye className="h-4 w-4" />
                    </Button>
                  </Link>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}

      {data && data.total > 0 && (
        <Pagination
          offset={data.offset}
          limit={data.limit}
          total={data.total}
          onPrevious={() => onPageChange(Math.max(0, offset - limit))}
          onNext={() => onPageChange(offset + limit)}
        />
      )}
    </div>
  )
}
