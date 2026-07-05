"use client"

import { useParams } from "next/navigation"
import { PageTransition } from "@/components/motion/PageTransition"
import { NotificationDetail } from "@/components/features/notifications/NotificationDetail"

export default function NotificationDetailPage() {
  const { id } = useParams<{ id: string }>()
  return (
    <PageTransition>
      <NotificationDetail notificationId={id} />
    </PageTransition>
  )
}
