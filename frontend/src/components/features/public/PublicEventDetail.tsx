"use client"

import { motion } from "framer-motion"
import Image from "next/image"
import Link from "next/link"
import {
  Calendar,
  MapPin,
  Clock,
  Users,
  GraduationCap,
  ArrowLeft,
  ExternalLink,
} from "lucide-react"
import { Badge } from "@/components/ui/Badge"
import { Button } from "@/components/ui/Button"
import { Skeleton } from "@/components/ui/Skeleton"
import { ParticipateButton } from "./ParticipateButton"
import { usePublicEvent } from "@/lib/hooks/usePublic"
import { EVENT_STATUS_LABELS, EVENT_STATUS_COLORS } from "@/types/events"
import { getCategoryColors, getCategoryMarker } from "@/types/categories"
import { getImageUrl } from "@/config"

interface PublicEventDetailProps {
  eventId: string
}

const MONTHS = [
  "января", "февраля", "марта", "апреля", "мая", "июня",
  "июля", "августа", "сентября", "октября", "ноября", "декабря",
]

function formatDate(dateStr: string) {
  const d = new Date(dateStr)
  return `${d.getDate()} ${MONTHS[d.getMonth()]} ${d.getFullYear()}`
}

function formatTime(timeStr: string | undefined) {
  if (!timeStr) return null
  return timeStr.slice(0, 5)
}

export function PublicEventDetail({ eventId }: PublicEventDetailProps) {
  const { data: event, isLoading, error } = usePublicEvent(eventId)

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-64 w-full rounded-2xl" />
      </div>
    )
  }

  if (error || !event) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <p className="text-lg text-foreground-muted">Мероприятие не найдено</p>
        <Link href="/">
          <Button variant="ghost" className="mt-4">
            <ArrowLeft className="mr-1.5 h-4 w-4" />
            Вернуться на главную
          </Button>
        </Link>
      </div>
    )
  }

  const statusColor = EVENT_STATUS_COLORS[event.status]
  const statusLabel = EVENT_STATUS_LABELS[event.status]

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <Link
        href="/"
        className="mb-6 inline-flex items-center gap-1.5 text-sm text-foreground-muted hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        На главную
      </Link>

      <div className="overflow-hidden rounded-3xl border border-border bg-white shadow-sm">
        {event.image_url && (
          <div className="relative h-64 w-full overflow-hidden sm:h-80">
            <Image
              src={getImageUrl(event.image_url)}
              alt={event.title}
              fill
              className="object-cover"
            />
          </div>
        )}

        <div className="p-6 sm:p-8">
          <div className="mb-4 flex flex-wrap items-center gap-3">
            <Badge className={statusColor}>{statusLabel}</Badge>
            <Badge className={getCategoryColors(event.category.name)}>
              {event.category.name}
            </Badge>
          </div>

          <h1 className="mb-4 text-2xl font-bold text-foreground sm:text-3xl">
            {event.title}
          </h1>

          <div className="mb-6 flex flex-wrap gap-x-6 gap-y-2 text-sm text-foreground-secondary">
            <span className="flex items-center gap-2">
              <Calendar className="h-4 w-4 text-primary-500" />
              {formatDate(event.start_date)}
            </span>
            {formatTime(event.start_time) && (
              <span className="flex items-center gap-2">
                <Clock className="h-4 w-4 text-primary-500" />
                {formatTime(event.start_time)}
                {formatTime(event.end_time) && ` — ${formatTime(event.end_time)}`}
              </span>
            )}
            <span className="flex items-center gap-2">
              <MapPin className="h-4 w-4 text-primary-500" />
              {event.location}
            </span>
            <span className="flex items-center gap-2">
              <Users className="h-4 w-4 text-primary-500" />
              {event.participants_count} участников
            </span>
            {event.target_audience && (
              <span className="flex items-center gap-2">
                <GraduationCap className="h-4 w-4 text-primary-500" />
                {event.target_audience}
              </span>
            )}
          </div>

          {event.short_description && (
            <p className="mb-4 text-base leading-relaxed text-foreground-secondary">
              {event.short_description}
            </p>
          )}

          <div className="mb-6 border-t border-border pt-6">
            <div className="prose prose-sm max-w-none text-foreground leading-relaxed whitespace-pre-line">
              {event.description}
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <ParticipateButton eventId={eventId} />
            {event.registration_url && (
              <a href={event.registration_url} target="_blank" rel="noopener noreferrer">
                <Button variant="secondary">
                  Ссылка на регистрацию
                  <ExternalLink className="ml-1.5 h-4 w-4" />
                </Button>
              </a>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  )
}
