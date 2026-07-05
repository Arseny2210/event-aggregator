"use client"

import Link from "next/link"
import { Pencil, ArrowLeft } from "lucide-react"
import { Card, CardHeader, CardTitle } from "@/components/ui/Card"
import { Badge } from "@/components/ui/Badge"
import { Button } from "@/components/ui/Button"
import { Spinner } from "@/components/ui/Spinner"
import { Alert } from "@/components/ui/Alert"
import { useAuth } from "@/lib/hooks/useAuth"
import { useEvent } from "@/lib/hooks/useEvents"
import { EVENT_STATUS_COLORS, EVENT_STATUS_LABELS } from "@/types/events"
import { DeleteEventButton } from "./DeleteEventDialog"

interface EventDetailProps {
  eventId: string
}

export function EventDetail({ eventId }: EventDetailProps) {
  const { user } = useAuth()
  const { data: event, isLoading, error } = useEvent(eventId)
  const canManage = user?.permissions?.includes("event:manage")

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Spinner className="h-8 w-8" />
      </div>
    )
  }

  if (error) {
    return (
      <Alert variant="error">
        Ошибка загрузки мероприятия: {error.message}
      </Alert>
    )
  }

  if (!event) {
    return <Alert variant="error">Мероприятие не найдено</Alert>
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Link href="/dashboard/events">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="mr-1 h-4 w-4" />
            Назад
          </Button>
        </Link>
        {canManage && (
          <div className="ml-auto flex gap-2">
            <Link href={`/dashboard/events/${event.id}/edit`}>
              <Button variant="secondary" size="sm">
                <Pencil className="mr-1 h-4 w-4" />
                Редактировать
              </Button>
            </Link>
            <DeleteEventButton
              eventId={event.id}
              eventTitle={event.title}
            />
          </div>
        )}
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div>
              <CardTitle className="text-xl">{event.title}</CardTitle>
              <Badge
                className={`mt-2 ${EVENT_STATUS_COLORS[event.status]}`}
              >
                {EVENT_STATUS_LABELS[event.status]}
              </Badge>
            </div>
          </div>
        </CardHeader>
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Детали</CardTitle>
          </CardHeader>
          <dl className="space-y-3 text-sm">
            <div>
              <dt className="font-medium text-foreground-secondary">Дата</dt>
              <dd className="text-foreground">
                {new Date(event.start_date).toLocaleDateString("ru-RU")}
                {event.start_time ? ` в ${event.start_time}` : ""}
              </dd>
            </div>
            {event.end_time && (
              <div>
                <dt className="font-medium text-foreground-secondary">
                  Время окончания
                </dt>
                <dd className="text-foreground">{event.end_time}</dd>
              </div>
            )}
            <div>
              <dt className="font-medium text-foreground-secondary">
                Место
              </dt>
              <dd className="text-foreground">{event.location}</dd>
            </div>
            <div>
              <dt className="font-medium text-foreground-secondary">
                Организатор
              </dt>
              <dd className="font-mono text-xs text-foreground">
                {event.organizer_id}
              </dd>
            </div>
            <div>
              <dt className="font-medium text-foreground-secondary">
                Категория
              </dt>
              <dd className="font-mono text-xs text-foreground">
                {event.category_id}
              </dd>
            </div>
          </dl>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Описание</CardTitle>
          </CardHeader>
          <div className="space-y-3 text-sm">
            {event.short_description && (
              <p className="text-foreground-secondary">
                {event.short_description}
              </p>
            )}
            <p className="whitespace-pre-wrap text-foreground">
              {event.description}
            </p>
          </div>
        </Card>
      </div>

      {(event.image_url || event.registration_url) && (
        <Card>
          <CardHeader>
            <CardTitle>Ссылки</CardTitle>
          </CardHeader>
          <dl className="space-y-2 text-sm">
            {event.image_url && (
              <div>
                <dt className="font-medium text-foreground-secondary">
                  Изображение
                </dt>
                <dd>
                  <a
                    href={event.image_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="break-all text-primary-600 hover:underline"
                  >
                    {event.image_url}
                  </a>
                </dd>
              </div>
            )}
            {event.registration_url && (
              <div>
                <dt className="font-medium text-foreground-secondary">
                  Регистрация
                </dt>
                <dd>
                  <a
                    href={event.registration_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="break-all text-primary-600 hover:underline"
                  >
                    {event.registration_url}
                  </a>
                </dd>
              </div>
            )}
          </dl>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Метаданные</CardTitle>
        </CardHeader>
        <dl className="space-y-2 text-xs text-foreground-muted">
          <div>
            <dt className="inline font-medium">ID:</dt>
            <dd className="ml-1 inline font-mono">{event.id}</dd>
          </div>
          <div>
            <dt className="inline font-medium">Создан:</dt>
            <dd className="ml-1 inline">
              {new Date(event.created_at).toLocaleString("ru-RU")}
            </dd>
          </div>
          <div>
            <dt className="inline font-medium">Обновлён:</dt>
            <dd className="ml-1 inline">
              {new Date(event.updated_at).toLocaleString("ru-RU")}
            </dd>
          </div>
        </dl>
      </Card>
    </div>
  )
}
