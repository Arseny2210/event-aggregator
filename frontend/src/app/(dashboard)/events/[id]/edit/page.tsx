"use client"

import { useParams } from "next/navigation"
import { EventForm } from "@/components/features/events/EventForm"
import { useEvent } from "@/lib/hooks/useEvents"
import { Spinner } from "@/components/ui/Spinner"
import { Alert } from "@/components/ui/Alert"

export default function EditEventPage() {
  const { id } = useParams<{ id: string }>()
  const { data: event, isLoading, error } = useEvent(id)

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Spinner className="h-8 w-8" />
      </div>
    )
  }

  if (error) {
    return <Alert variant="error">Failed to load event: {error.message}</Alert>
  }

  if (!event) {
    return <Alert variant="error">Event not found</Alert>
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Edit Event</h1>
      <EventForm event={event} isEditing />
    </div>
  )
}
