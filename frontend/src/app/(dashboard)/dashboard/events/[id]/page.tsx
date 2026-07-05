"use client"

import { useParams } from "next/navigation"
import { PageTransition } from "@/components/motion/PageTransition"
import { EventDetail } from "@/components/features/events/EventDetail"

export default function EventDetailPage() {
  const { id } = useParams<{ id: string }>()
  return (
    <PageTransition>
      <EventDetail eventId={id} />
    </PageTransition>
  )
}
