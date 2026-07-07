"use client"

import Link from "next/link"
import { ArrowLeft } from "lucide-react"
import { Card, CardHeader, CardTitle } from "@/components/ui/Card"
import { Badge } from "@/components/ui/Badge"
import { Progress } from "@/components/ui/Progress"
import { Button } from "@/components/ui/Button"
import { Spinner } from "@/components/ui/Spinner"
import { Alert } from "@/components/ui/Alert"
import { useAuth } from "@/lib/hooks/useAuth"
import { useImport } from "@/lib/hooks/useImports"
import { IMPORT_STATUS_COLORS, IMPORT_STATUS_LABELS } from "@/types/imports"
import { DeleteImportButton } from "./DeleteImportDialog"
import { ImportRowResults } from "./ImportRowResults"

interface ImportDetailProps {
  importId: string
}

export function ImportDetail({ importId }: ImportDetailProps) {
  const { user } = useAuth()
  const { data: job, isLoading, error } = useImport(importId)
  const isAdmin = user?.role?.name === "administrator"

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Spinner className="h-8 w-8" />
      </div>
    )
  }

  if (error) {
    return (
      <Alert variant="error">
        Ошибка загрузки импорта: {error.message}
      </Alert>
    )
  }

  if (!job) {
    return <Alert variant="error">Импорт не найден</Alert>
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Link href="/dashboard/imports">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="mr-1 h-4 w-4" />
            Назад
          </Button>
        </Link>
        {isAdmin && (
          <div className="ml-auto">
            <DeleteImportButton
              importId={job.id}
              importFilename={job.filename}
            />
          </div>
        )}
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div>
              <CardTitle className="text-xl">{job.filename}</CardTitle>
              <Badge
                className={`mt-2 ${IMPORT_STATUS_COLORS[job.status]}`}
              >
                {IMPORT_STATUS_LABELS[job.status]}
              </Badge>
            </div>
          </div>
        </CardHeader>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Прогресс</CardTitle>
        </CardHeader>
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <Progress
              value={job.summary.progress_percent}
              className="flex-1"
            />
            <span className="text-sm font-medium text-foreground">
              {job.summary.progress_percent}%
            </span>
          </div>
          <div className="grid grid-cols-2 gap-4 text-sm sm:grid-cols-4">
            <div>
              <dt className="text-foreground-muted">Всего</dt>
              <dd className="font-medium text-foreground">
                {job.summary.total_rows}
              </dd>
            </div>
            <div>
              <dt className="text-foreground-muted">Обработано</dt>
              <dd className="font-medium text-foreground">
                {job.summary.processed_rows}
              </dd>
            </div>
            <div>
              <dt className="text-foreground-muted">Импортировано</dt>
              <dd className="font-medium text-green-600">
                {job.summary.imported_rows}
              </dd>
            </div>
            <div>
              <dt className="text-foreground-muted">Ошибок</dt>
              <dd className="font-medium text-red-600">
                {job.summary.failed_rows}
              </dd>
            </div>
          </div>
        </div>
      </Card>

      {(job.summary.started_at || job.summary.finished_at) && (
        <Card>
          <CardHeader>
            <CardTitle>Время</CardTitle>
          </CardHeader>
          <dl className="grid grid-cols-2 gap-4 text-sm sm:grid-cols-3">
            {job.summary.started_at && (
              <div>
                <dt className="text-foreground-muted">Начало</dt>
                <dd className="text-foreground">
                  {new Date(job.summary.started_at).toLocaleString("ru-RU")}
                </dd>
              </div>
            )}
            {job.summary.finished_at && (
              <div>
                <dt className="text-foreground-muted">Окончание</dt>
                <dd className="text-foreground">
                  {new Date(job.summary.finished_at).toLocaleString("ru-RU")}
                </dd>
              </div>
            )}
            <div>
              <dt className="text-foreground-muted">Длительность</dt>
              <dd className="text-foreground">{job.summary.duration}с</dd>
            </div>
          </dl>
        </Card>
      )}

      <ImportRowResults importId={importId} />
    </div>
  )
}
