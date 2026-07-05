"use client"

import { useState } from "react"
import { Card, CardHeader, CardTitle } from "@/components/ui/Card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/Table"
import { Badge } from "@/components/ui/Badge"
import { Pagination } from "@/components/ui/Pagination"
import { Spinner } from "@/components/ui/Spinner"
import { Select } from "@/components/ui/Select"
import { useImportRows } from "@/lib/hooks/useImports"
import type { ImportRowStatus } from "@/types/imports"
import {
  IMPORT_ROW_STATUS_COLORS,
  IMPORT_ROW_STATUS_LABELS,
} from "@/types/imports"

interface ImportRowResultsProps {
  importId: string
}

const STATUS_OPTIONS = [
  { value: "", label: "Все статусы" },
  { value: "imported", label: "Импортировано" },
  { value: "warning", label: "Предупреждение" },
  { value: "failed", label: "Ошибка" },
]

export function ImportRowResults({ importId }: ImportRowResultsProps) {
  const [offset, setOffset] = useState(0)
  const [status, setStatus] = useState("")
  const limit = 50

  const params = {
    offset,
    limit,
    status: (status || undefined) as ImportRowStatus | undefined,
  }
  const { data, isLoading } = useImportRows(importId, params)

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Результаты строк</CardTitle>
          <div className="w-36">
            <Select
              options={STATUS_OPTIONS}
              value={status}
              onChange={(e) => {
                setStatus(e.target.value)
                setOffset(0)
              }}
            />
          </div>
        </div>
      </CardHeader>

      {isLoading && (
        <div className="flex justify-center py-6">
          <Spinner />
        </div>
      )}

      {data && data.items.length === 0 && (
        <p className="px-6 pb-6 text-sm text-foreground-muted">
          Нет результатов.
        </p>
      )}

      {data && data.items.length > 0 && (
        <>
          <Table>
            <TableHead>
              <TableRow>
                <TableHeader>Строка</TableHeader>
                <TableHeader>Статус</TableHeader>
                <TableHeader>Ошибка</TableHeader>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.items.map((row) => (
                <TableRow key={row.id}>
                  <TableCell className="w-20">#{row.row_number}</TableCell>
                  <TableCell>
                    <Badge
                      className={
                        IMPORT_ROW_STATUS_COLORS[row.status]
                      }
                    >
                      {IMPORT_ROW_STATUS_LABELS[row.status]}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    {row.error_message ? (
                      <div>
                        <span className="text-xs font-medium text-red-600">
                          {row.error_code}
                        </span>
                        <p className="text-xs text-foreground-muted">
                          {row.error_message}
                        </p>
                      </div>
                    ) : (
                      <span className="text-xs text-foreground-muted">
                        —
                      </span>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <div className="p-4">
            <Pagination
              offset={data.offset}
              limit={data.limit}
              total={data.total}
              onPrevious={() => setOffset(Math.max(0, offset - limit))}
              onNext={() => setOffset(offset + limit)}
            />
          </div>
        </>
      )}
    </Card>
  )
}
