"use client"

import Link from "next/link"
import { motion } from "framer-motion"
import { Eye, Send } from "lucide-react"
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
import { Alert } from "@/components/ui/Alert"
import { Button } from "@/components/ui/Button"
import { Select } from "@/components/ui/Select"
import { useNotifications } from "@/lib/hooks/useNotifications"
import { EmptyState } from "@/components/layout/EmptyState"
import {
  NOTIF_CHANNEL_LABELS,
  NOTIF_PRIORITY_COLORS,
  NOTIF_PRIORITY_LABELS,
  NOTIF_STATUS_COLORS,
  NOTIF_STATUS_LABELS,
  NOTIF_TEMPLATE_LABELS,
} from "@/types/notifications"
import type { NotificationStatus } from "@/types/notifications"

interface NotificationListProps {
  offset: number
  limit: number
  status: string
  onPageChange: (offset: number) => void
  onStatusChange: (status: string) => void
  onSendClick: () => void
}

const STATUS_OPTIONS = [
  { value: "", label: "Все статусы" },
  { value: "pending", label: "Ожидание" },
  { value: "sent", label: "Отправлено" },
  { value: "failed", label: "Ошибка" },
  { value: "retrying", label: "Повтор" },
]

export function NotificationList({
  offset,
  limit,
  status,
  onPageChange,
  onStatusChange,
  onSendClick,
}: NotificationListProps) {
  const params = {
    offset,
    limit,
    status: (status || undefined) as NotificationStatus | undefined,
  }
  const { data, isLoading, error } = useNotifications(params)

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <div className="w-44">
          <Select
            options={STATUS_OPTIONS}
            value={status}
            onChange={(e) => {
              onStatusChange(e.target.value)
              onPageChange(0)
            }}
          />
        </div>
        <div className="ml-auto">
          <Button size="sm" onClick={onSendClick}>
            <Send className="mr-1 h-4 w-4" />
            Отправить
          </Button>
        </div>
      </div>

      {isLoading && (
        <div className="flex items-center justify-center py-12">
          <Spinner className="h-8 w-8" />
        </div>
      )}

      {error && (
        <Alert variant="error">
          Ошибка загрузки уведомлений: {error.message}
        </Alert>
      )}

      {data && data.items.length === 0 && (
        <EmptyState
          title="Уведомления не найдены"
          description="Отправьте первое уведомление"
        />
      )}

      {data && data.items.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <Table>
            <TableHead>
              <TableRow>
                <TableHeader>Получатель</TableHeader>
                <TableHeader>Шаблон</TableHeader>
                <TableHeader>Канал</TableHeader>
                <TableHeader>Статус</TableHeader>
                <TableHeader>Приоритет</TableHeader>
                <TableHeader>Создано</TableHeader>
                <TableHeader className="w-16">Действия</TableHeader>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.items.map((n) => (
                <TableRow key={n.id}>
                  <TableCell className="font-medium">
                    {n.recipient}
                  </TableCell>
                  <TableCell>
                    {NOTIF_TEMPLATE_LABELS[n.template_type]}
                  </TableCell>
                  <TableCell>
                    {NOTIF_CHANNEL_LABELS[n.channel]}
                  </TableCell>
                  <TableCell>
                    <Badge className={NOTIF_STATUS_COLORS[n.status]}>
                      {NOTIF_STATUS_LABELS[n.status]}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge className={NOTIF_PRIORITY_COLORS[n.priority]}>
                      {NOTIF_PRIORITY_LABELS[n.priority]}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-foreground-muted">
                    {new Date(n.created_at).toLocaleDateString("ru-RU")}
                  </TableCell>
                  <TableCell>
                    <Link
                      href={`/dashboard/notifications/${n.id}`}
                    >
                      <Button
                        variant="ghost"
                        size="sm"
                        aria-label="Просмотр"
                      >
                        <Eye className="h-4 w-4" />
                      </Button>
                    </Link>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </motion.div>
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
