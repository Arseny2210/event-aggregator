"use client"

import { useParams } from "next/navigation"
import { NotificationDetail } from "@/components/features/notifications/NotificationDetail"

export default function NotificationDetailPage() {
  const { id } = useParams<{ id: string }>()
  return <NotificationDetail notificationId={id} />
}
