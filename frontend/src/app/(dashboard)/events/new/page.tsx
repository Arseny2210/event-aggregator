"use client"

import { EventForm } from "@/components/features/events/EventForm"

export default function NewEventPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Create Event</h1>
      <EventForm />
    </div>
  )
}
