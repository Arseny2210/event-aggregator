"use client"

import { useParams } from "next/navigation"
import { EventDetail } from "@/components/features/events/EventDetail"

export default function EventDetailPage() {
  const { id } = useParams<{ id: string }>()
  return <EventDetail eventId={id} />
}
