"use client"

import { PageTransition } from "@/components/motion/PageTransition"
import { EventForm } from "@/components/features/events/EventForm"

export default function NewEventPage() {
  return (
    <PageTransition>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">
            Создание мероприятия
          </h1>
          <p className="text-sm text-foreground-secondary">
            Заполните форму для добавления нового события
          </p>
        </div>
        <EventForm />
      </div>
    </PageTransition>
  )
}
