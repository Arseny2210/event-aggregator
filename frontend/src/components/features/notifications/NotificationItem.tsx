"use client"

import { Check, Trash2 } from "lucide-react"
import type { Notification } from "@/types/notifications"

interface NotificationItemProps {
  notification: Notification
  onMarkAsRead: (id: string) => void
  onDelete: (id: string) => void
}

export function NotificationItem({ notification, onMarkAsRead, onDelete }: NotificationItemProps) {
  const isUnread = !notification.read_at

  return (
    <div
      className={`border-b border-border p-4 last:border-b-0 ${
        isUnread ? "bg-blue-50" : ""
      }`}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0 flex-1">
          <p className="text-sm font-medium">{notification.subject}</p>
          <p className="mt-1 text-xs text-muted-foreground">
            {(notification.payload?.rendered_body as string) || ""}
          </p>
          <p className="mt-2 text-xs text-muted-foreground">
            {new Date(notification.sent_at ?? notification.created_at).toLocaleString("ru-RU")}
          </p>
        </div>
        <div className="flex shrink-0 gap-1">
          {isUnread && (
            <button
              onClick={() => onMarkAsRead(notification.id)}
              className="rounded p-1 text-muted-foreground hover:text-foreground"
              title="Прочитано"
            >
              <Check className="h-4 w-4" />
            </button>
          )}
          <button
            onClick={() => onDelete(notification.id)}
            className="rounded p-1 text-muted-foreground hover:text-red-500"
            title="Удалить"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  )
}
