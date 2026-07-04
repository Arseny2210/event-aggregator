"use client"

import { useState } from "react"
import { SendNotificationModal } from "@/components/features/notifications/SendNotificationModal"
import { NotificationList } from "@/components/features/notifications/NotificationList"

export default function NotificationsPage() {
  const [offset, setOffset] = useState(0)
  const [status, setStatus] = useState("")
  const [sendOpen, setSendOpen] = useState(false)
  const limit = 20

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Notifications</h1>
      <NotificationList
        offset={offset}
        limit={limit}
        status={status}
        onPageChange={setOffset}
        onStatusChange={setStatus}
        onSendClick={() => setSendOpen(true)}
      />
      <SendNotificationModal open={sendOpen} onClose={() => setSendOpen(false)} />
    </div>
  )
}
