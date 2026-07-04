"use client"

import Link from "next/link"
import { Eye, Send } from "lucide-react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/Table"
import { Badge } from "@/components/ui/Badge"
import { Pagination } from "@/components/ui/Pagination"
import { Spinner } from "@/components/ui/Spinner"
import { Alert } from "@/components/ui/Alert"
import { Button } from "@/components/ui/Button"
import { useNotifications } from "@/lib/hooks/useNotifications"
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

export function NotificationList({
  offset, limit, status, onPageChange, onStatusChange, onSendClick,
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
        <select
          className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900"
          value={status}
          onChange={(e) => { onStatusChange(e.target.value); onPageChange(0) }}
        >
          <option value="">All statuses</option>
          <option value="pending">Pending</option>
          <option value="sent">Sent</option>
          <option value="failed">Failed</option>
          <option value="retrying">Retrying</option>
        </select>
        <div className="ml-auto">
          <Button size="sm" onClick={onSendClick}>
            <Send className="mr-1 h-4 w-4" />
            Send
          </Button>
        </div>
      </div>

      {isLoading && (
        <div className="flex items-center justify-center py-12">
          <Spinner className="h-8 w-8" />
        </div>
      )}

      {error && <Alert variant="error">Failed to load notifications: {error.message}</Alert>}

      {data && data.items.length === 0 && (
        <div className="py-12 text-center">
          <p className="text-slate-500">No notifications found.</p>
        </div>
      )}

      {data && data.items.length > 0 && (
        <Table>
          <TableHead>
            <TableRow>
              <TableHeader>Recipient</TableHeader>
              <TableHeader>Template</TableHeader>
              <TableHeader>Channel</TableHeader>
              <TableHeader>Status</TableHeader>
              <TableHeader>Priority</TableHeader>
              <TableHeader>Created</TableHeader>
              <TableHeader className="w-16">Actions</TableHeader>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.items.map((n) => (
              <TableRow key={n.id}>
                <TableCell className="font-medium">{n.recipient}</TableCell>
                <TableCell>{NOTIF_TEMPLATE_LABELS[n.template_type]}</TableCell>
                <TableCell>{NOTIF_CHANNEL_LABELS[n.channel]}</TableCell>
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
                <TableCell className="text-slate-500">
                  {new Date(n.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  <Link href={`/dashboard/notifications/${n.id}`}>
                    <Button variant="ghost" size="sm" aria-label="View notification">
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
