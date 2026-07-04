"use client"

import Link from "next/link"
import { ArrowLeft } from "lucide-react"
import { Card, CardHeader, CardTitle } from "@/components/ui/Card"
import { Badge } from "@/components/ui/Badge"
import { Button } from "@/components/ui/Button"
import { Spinner } from "@/components/ui/Spinner"
import { Alert } from "@/components/ui/Alert"
import { useNotification } from "@/lib/hooks/useNotifications"
import {
  NOTIF_CHANNEL_LABELS,
  NOTIF_PRIORITY_COLORS,
  NOTIF_PRIORITY_LABELS,
  NOTIF_STATUS_COLORS,
  NOTIF_STATUS_LABELS,
  NOTIF_TEMPLATE_LABELS,
} from "@/types/notifications"

interface NotificationDetailProps {
  notificationId: string
}

export function NotificationDetail({ notificationId }: NotificationDetailProps) {
  const { data: notif, isLoading, error } = useNotification(notificationId)

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Spinner className="h-8 w-8" />
      </div>
    )
  }

  if (error) {
    return <Alert variant="error">Failed to load notification: {error.message}</Alert>
  }

  if (!notif) {
    return <Alert variant="error">Notification not found</Alert>
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Link href="/dashboard/notifications">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="mr-1 h-4 w-4" />
            Back
          </Button>
        </Link>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-start gap-3">
            <div className="flex-1">
              <CardTitle className="text-xl">
                {notif.subject || NOTIF_TEMPLATE_LABELS[notif.template_type]}
              </CardTitle>
              <div className="mt-2 flex gap-2">
                <Badge className={NOTIF_STATUS_COLORS[notif.status]}>
                  {NOTIF_STATUS_LABELS[notif.status]}
                </Badge>
                <Badge className={NOTIF_PRIORITY_COLORS[notif.priority]}>
                  {NOTIF_PRIORITY_LABELS[notif.priority]}
                </Badge>
              </div>
            </div>
          </div>
        </CardHeader>
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Details</CardTitle>
          </CardHeader>
          <dl className="space-y-3 text-sm">
            <div>
              <dt className="font-medium text-slate-600">Recipient</dt>
              <dd className="text-slate-900">{notif.recipient}</dd>
            </div>
            <div>
              <dt className="font-medium text-slate-600">Channel</dt>
              <dd className="text-slate-900">{NOTIF_CHANNEL_LABELS[notif.channel]}</dd>
            </div>
            <div>
              <dt className="font-medium text-slate-600">Template</dt>
              <dd className="text-slate-900">{NOTIF_TEMPLATE_LABELS[notif.template_type]}</dd>
            </div>
            <div>
              <dt className="font-medium text-slate-600">Attempts</dt>
              <dd className="text-slate-900">{notif.attempts}</dd>
            </div>
          </dl>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Payload</CardTitle>
          </CardHeader>
          <pre className="overflow-auto text-xs text-slate-700 whitespace-pre-wrap max-h-64">
            {JSON.stringify(notif.payload, null, 2)}
          </pre>
        </Card>
      </div>

      {notif.error_message && (
        <Card>
          <CardHeader>
            <CardTitle>Error</CardTitle>
          </CardHeader>
          <p className="text-sm text-red-700">{notif.error_message}</p>
        </Card>
      )}

      <dl className="grid grid-cols-3 gap-4 text-sm">
        <div>
          <dt className="text-slate-500">Created</dt>
          <dd className="text-slate-900">{new Date(notif.created_at).toLocaleString()}</dd>
        </div>
        {notif.sent_at && (
          <div>
            <dt className="text-slate-500">Sent</dt>
            <dd className="text-slate-900">{new Date(notif.sent_at).toLocaleString()}</dd>
          </div>
        )}
        {notif.scheduled_at && (
          <div>
            <dt className="text-slate-500">Scheduled</dt>
            <dd className="text-slate-900">{new Date(notif.scheduled_at).toLocaleString()}</dd>
          </div>
        )}
      </dl>
    </div>
  )
}
