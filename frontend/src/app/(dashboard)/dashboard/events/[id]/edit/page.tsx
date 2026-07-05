"use client"

import { useParams } from "next/navigation"
import { PageTransition } from "@/components/motion/PageTransition"
import { EventForm } from "@/components/features/events/EventForm"
import { useEvent } from "@/lib/hooks/useEvents"
import { Spinner } from "@/components/ui/Spinner"
import { Alert } from "@/components/ui/Alert"

export default function EditEventPage() {
  const { id } = useParams<{ id: string }>()
  const { data: event, isLoading, error } = useEvent(id)

  if (isLoading) {
    return (
      <PageTransition>
        <div className="flex items-center justify-center py-12">
          <Spinner className="h-8 w-8" />
        </div>
      </PageTransition>
    )
  }

  if (error) {
    return (
      <PageTransition>
        <Alert variant="error">
          Ошибка загрузки мероприятия: {error.message}
        </Alert>
      </PageTransition>
    )
  }

  if (!event) {
    return (
      <PageTransition>
        <Alert variant="error">Мероприятие не найдено</Alert>
      </PageTransition>
    )
  }

  return (
    <PageTransition>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">
            Редактирование мероприятия
          </h1>
          <p className="text-sm text-foreground-secondary">
            Внесите изменения в мероприятие
          </p>
        </div>
        <EventForm event={event} isEditing />
      </div>
    </PageTransition>
  )
}
