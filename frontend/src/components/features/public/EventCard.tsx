"use client"

import Link from "next/link"
import { motion } from "framer-motion"
import { Calendar, MapPin, Users, Clock, ExternalLink } from "lucide-react"
import { Badge } from "@/components/ui/Badge"
import { ParticipateButton } from "@/components/features/public/ParticipateButton"
import type { Event } from "@/types/events"
import { getCategoryColors, getCategoryMarker } from "@/types/categories"

interface EventCardProps {
  event: Event
}

const MONTHS = [
  "янв", "фев", "мар", "апр", "май", "июн",
  "июл", "авг", "сен", "окт", "ноя", "дек",
]

function formatDate(dateStr: string) {
  const d = new Date(dateStr)
  return `${d.getDate()} ${MONTHS[d.getMonth()]} ${d.getFullYear()}`
}

function formatTime(timeStr: string | undefined) {
  if (!timeStr) return null
  return timeStr.slice(0, 5)
}

export function EventCard({ event }: EventCardProps) {
  return (
    <Link href={`/events/${event.id}`}>
      <motion.div
        whileHover={{ y: -3 }}
        className="group cursor-pointer rounded-2xl border border-border bg-white p-5 shadow-sm transition-all hover:border-primary-200 hover:shadow-md"
      >
        <div className="mb-3 flex items-start justify-between gap-3">
          <div className="flex items-start gap-3 min-w-0">
            <div
              className={`mt-1.5 h-3 w-3 shrink-0 rounded-full ${getCategoryMarker(event.category.name)}`}
            />
            <h3 className="text-base font-semibold text-foreground line-clamp-2 group-hover:text-primary-600 transition-colors">
              {event.title}
            </h3>
          </div>
          <Badge className={`${getCategoryColors(event.category.name)} shrink-0`}>
            {event.category.name}
          </Badge>
        </div>

        {event.short_description && (
          <p className="mb-3 pl-6 text-sm leading-relaxed text-foreground-secondary line-clamp-2">
            {event.short_description}
          </p>
        )}

        <div className="flex flex-wrap gap-x-4 gap-y-1.5 pl-6 text-sm text-foreground-muted">
          <span className="flex items-center gap-1.5">
            <Calendar className="h-3.5 w-3.5" />
            {formatDate(event.start_date)}
          </span>
          {formatTime(event.start_time) && (
            <span className="flex items-center gap-1.5">
              <Clock className="h-3.5 w-3.5" />
              {formatTime(event.start_time)}
            </span>
          )}
          <span className="flex items-center gap-1.5">
            <MapPin className="h-3.5 w-3.5" />
            {event.location}
          </span>
          <span className="flex items-center gap-1.5">
            <Users className="h-3.5 w-3.5" />
            {event.participants_count}
          </span>
        </div>

        {event.target_audience && (
          <div className="mt-2 pl-6">
            <Badge className="bg-primary-50 text-primary-700 text-xs">
              {event.target_audience}
            </Badge>
          </div>
        )}

        <div className="mt-3 flex flex-wrap items-center gap-2 pl-6">
          {event.participation_enabled && (
            <div onClick={(e) => e.preventDefault()}>
              <ParticipateButton eventId={event.id} />
            </div>
          )}
          {event.registration_url && (
            <a
              href={event.registration_url}
              target="_blank"
              rel="noopener noreferrer"
              onClick={(e) => e.stopPropagation()}
              className="inline-flex items-center gap-1 text-xs font-medium text-primary-600 hover:text-primary-700"
            >
              <ExternalLink className="h-3 w-3" />
              Регистрация
            </a>
          )}
        </div>
      </motion.div>
    </Link>
  )
}
