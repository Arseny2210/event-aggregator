"use client"

import { useState, useMemo, useRef, useEffect, useCallback } from "react"
import { motion, AnimatePresence } from "framer-motion"
import {
  CalendarDays,
  Clock,
  Eye,
  EyeOff,
  Loader2,
  Sparkles,
} from "lucide-react"
import { Button } from "@/components/ui/Button"
import { EventCard } from "./EventCard"
import type { Event } from "@/types/events"

interface TimelineViewProps {
  events: Event[]
  onLoadMore?: () => void
  hasMore?: boolean
  isLoadingMore?: boolean
}

const MONTHS = [
  "января", "февраля", "марта", "апреля", "мая", "июня",
  "июля", "августа", "сентября", "октября", "ноября", "декабря",
]

function formatGroupDate(dateStr: string) {
  const d = new Date(dateStr)
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)

  const fmtDate = (dd: Date) =>
    `${dd.getDate()} ${MONTHS[dd.getMonth()]} ${dd.getFullYear()}`

  if (d.toDateString() === today.toDateString()) return "Сегодня"
  if (d.toDateString() === yesterday.toDateString()) return "Вчера"
  if (d.toDateString() === tomorrow.toDateString()) return "Завтра"
  return fmtDate(d)
}

function isDateHighlighted(dateStr: string) {
  const d = new Date(dateStr)
  const today = new Date()
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)
  return (
    d.toDateString() === today.toDateString() ||
    d.toDateString() === tomorrow.toDateString()
  )
}

function isPast(dateStr: string) {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return new Date(dateStr) < today
}

export function TimelineView({
  events,
  onLoadMore,
  hasMore = false,
  isLoadingMore = false,
}: TimelineViewProps) {
  const [showPast, setShowPast] = useState(false)
  const sentinelRef = useRef<HTMLDivElement>(null)

  const grouped = useMemo(() => {
    const groups = new Map<string, Event[]>()
    const sorted = [...events].sort(
      (a, b) => new Date(a.start_date).getTime() - new Date(b.start_date).getTime(),
    )
    const filtered = showPast
      ? sorted
      : sorted.filter((e) => !isPast(e.start_date))
    for (const event of filtered) {
      const key = event.start_date
      const existing = groups.get(key) ?? []
      existing.push(event)
      groups.set(key, existing)
    }
    return Array.from(groups.entries())
  }, [events, showPast])

  const pastCount = events.filter((e) => isPast(e.start_date)).length

  useEffect(() => {
    if (!onLoadMore || !hasMore) return
    const el = sentinelRef.current
    if (!el) return
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) onLoadMore()
      },
      { rootMargin: "200px" },
    )
    observer.observe(el)
    return () => observer.disconnect()
  }, [onLoadMore, hasMore])

  return (
    <div>
      <div className="mb-5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Clock className="h-5 w-5 text-primary-600" />
          <h2 className="text-xl font-bold text-foreground">Лента мероприятий</h2>
        </div>
        {pastCount > 0 && (
          <Button variant="ghost" size="sm" onClick={() => setShowPast((v) => !v)}>
            {showPast ? (
              <>
                <EyeOff className="mr-1.5 h-4 w-4" />
                Скрыть прошедшие
              </>
            ) : (
              <>
                <Eye className="mr-1.5 h-4 w-4" />
                Показать прошедшие ({pastCount})
              </>
            )}
          </Button>
        )}
      </div>

      <AnimatePresence mode="popLayout">
        {grouped.length === 0 && !isLoadingMore ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-border bg-surface-secondary py-16"
          >
            <CalendarDays className="mb-3 h-10 w-10 text-foreground-muted" />
            <p className="text-sm text-foreground-muted">Нет мероприятий</p>
          </motion.div>
        ) : (
          <div className="space-y-10">
            {grouped.map(([dateStr, dateEvents], groupIdx) => {
              const highlighted = isDateHighlighted(dateStr)
              return (
                <motion.div
                  key={dateStr}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: groupIdx * 0.05 }}
                  layout
                >
                  <div className="mb-4 flex items-center gap-3">
                    <div
                      className={`flex h-8 items-center justify-center rounded-full px-4 ${
                        highlighted
                          ? "bg-primary-600 text-white shadow-sm"
                          : "bg-primary-100 text-primary-700"
                      }`}
                    >
                      {highlighted && (
                        <Sparkles className="mr-1.5 h-3.5 w-3.5" />
                      )}
                      <span className="text-sm font-bold">
                        {formatGroupDate(dateStr)}
                      </span>
                    </div>
                    <div className="h-px flex-1 bg-border" />
                  </div>
                  <div className="space-y-4">
                    {dateEvents.map((event, eventIdx) => (
                      <motion.div
                        key={event.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: eventIdx * 0.03 }}
                      >
                        <EventCard event={event} />
                      </motion.div>
                    ))}
                  </div>
                </motion.div>
              )
            })}
            {isLoadingMore && (
              <div className="flex justify-center py-6">
                <Loader2 className="h-6 w-6 animate-spin text-primary-500" />
              </div>
            )}
            <div ref={sentinelRef} className="h-4" />
          </div>
        )}
      </AnimatePresence>
    </div>
  )
}
