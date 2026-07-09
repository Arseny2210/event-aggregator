"use client"

import { useState, useEffect, useRef } from "react"
import { Bell } from "lucide-react"
import {
  usePublicNotifications,
  useMarkNotificationAsRead,
  useDeleteNotification,
} from "@/lib/hooks/usePublicNotifications"
import { NotificationItem } from "./NotificationItem"

interface NotificationBellProps {
  sessionId: string | undefined
}

export function NotificationBell({ sessionId }: NotificationBellProps) {
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)
  const { data } = usePublicNotifications(sessionId)
  const markAsRead = useMarkNotificationAsRead()
  const deleteNotification = useDeleteNotification()

  const notifications = data?.items ?? []
  const unreadCount = notifications.filter((n) => !n.read_at).length

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }
    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside)
    }
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [isOpen])

  const handleMarkAsRead = (notificationId: string) => {
    if (!sessionId) return
    markAsRead.mutate({ notificationId, sessionId })
  }

  const handleDelete = (notificationId: string) => {
    if (!sessionId) return
    deleteNotification.mutate({ notificationId, sessionId })
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative rounded-lg bg-white p-2 text-foreground hover:bg-surface-tertiary"
        aria-label="Уведомления"
      >
        <Bell className="h-5 w-5" />
        {unreadCount > 0 && (
          <span className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-xs text-white">
            {unreadCount > 9 ? "9+" : unreadCount}
          </span>
        )}
      </button>

      {isOpen && (
        <div className="absolute right-0 top-full z-50 mt-2 w-80 rounded-lg border border-border bg-white shadow-lg">
          <div className="border-b border-border px-4 py-3">
            <h3 className="text-sm font-semibold">Уведомления</h3>
          </div>
          <div className="max-h-96 overflow-y-auto">
            {!sessionId ? (
              <div className="px-4 py-8 text-center text-sm text-muted-foreground">
                Войдите, чтобы получать уведомления
              </div>
            ) : notifications.length === 0 ? (
              <div className="px-4 py-8 text-center text-sm text-muted-foreground">
                Нет уведомлений
              </div>
            ) : (
              notifications.map((notification) => (
                <NotificationItem
                  key={notification.id}
                  notification={notification}
                  onMarkAsRead={handleMarkAsRead}
                  onDelete={handleDelete}
                />
              ))
            )}
          </div>
        </div>
      )}
    </div>
  )
}
