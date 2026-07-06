"use client"

import { useState, useCallback, useMemo } from "react"
import { motion, AnimatePresence } from "framer-motion"
import {
  ChevronLeft,
  ChevronRight,
  CalendarDays,
  MapPin,
  Clock,
} from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/Button"
import { Badge } from "@/components/ui/Badge"
import type { Event } from "@/types/events"
import { getCategoryColors, getCategoryMarker } from "@/types/categories"

interface CalendarViewProps {
  events: Event[]
}

const DAYS_OF_WEEK = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
const MONTHS = [
  "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
  "Июль", "Август", "Сентябрь", "Окторябрь", "Ноябрь", "Декабрь",
]

function getDaysInMonth(year: number, month: number): number {
  return new Date(year, month + 1, 0).getDate()
}

function getStartDayOfWeek(year: number, month: number): number {
  const day = new Date(year, month, 1).getDay()
  return day === 0 ? 6 : day - 1
}

function formatTime(timeStr: string | undefined) {
  if (!timeStr) return null
  return timeStr.slice(0, 5)
}

export function CalendarView({ events }: CalendarViewProps) {
  const today = useMemo(() => new Date(), [])
  const [currentYear, setCurrentYear] = useState(today.getFullYear())
  const [currentMonth, setCurrentMonth] = useState(today.getMonth())
  const [selectedDate, setSelectedDate] = useState<string | null>(null)
  const [selectedEvents, setSelectedEvents] = useState<Event[]>([])

  const eventsByDate = new Map<string, Event[]>()
  for (const event of events) {
    const key = event.start_date
    const existing = eventsByDate.get(key) ?? []
    existing.push(event)
    eventsByDate.set(key, existing)
  }

  const daysInMonth = getDaysInMonth(currentYear, currentMonth)
  const startDay = getStartDayOfWeek(currentYear, currentMonth)

  const prevMonth = useCallback(() => {
    if (currentMonth === 0) {
      setCurrentYear((y) => y - 1)
      setCurrentMonth(11)
    } else {
      setCurrentMonth((m) => m - 1)
    }
    setSelectedDate(null)
    setSelectedEvents([])
  }, [currentMonth])

  const nextMonth = useCallback(() => {
    if (currentMonth === 11) {
      setCurrentYear((y) => y + 1)
      setCurrentMonth(0)
    } else {
      setCurrentMonth((m) => m + 1)
    }
    setSelectedDate(null)
    setSelectedEvents([])
  }, [currentMonth])

  const goToToday = useCallback(() => {
    setCurrentYear(today.getFullYear())
    setCurrentMonth(today.getMonth())
    setSelectedDate(null)
    setSelectedEvents([])
  }, [today])

  const handleDayClick = (day: number) => {
    const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`
    if (selectedDate === dateStr) {
      setSelectedDate(null)
      setSelectedEvents([])
    } else {
      setSelectedDate(dateStr)
      setSelectedEvents(eventsByDate.get(dateStr) ?? [])
    }
  }

  const isToday = (day: number) =>
    currentYear === today.getFullYear() &&
    currentMonth === today.getMonth() &&
    day === today.getDate()

  return (
    <div>
      <div className="mb-5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <CalendarDays className="h-5 w-5 text-primary-600" />
          <h2 className="text-xl font-bold text-foreground">
            {MONTHS[currentMonth]} {currentYear}
          </h2>
        </div>
        <div className="flex items-center gap-1">
          <Button variant="ghost" size="sm" onClick={goToToday}>
            Сегодня
          </Button>
          <div className="flex gap-0.5">
            <Button variant="ghost" size="sm" onClick={prevMonth}>
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" onClick={nextMonth}>
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      <div className="overflow-hidden rounded-2xl border border-border bg-white shadow-sm">
        <div className="grid grid-cols-7 border-b border-border bg-surface-secondary">
          {DAYS_OF_WEEK.map((day) => (
            <div
              key={day}
              className="py-2.5 text-center text-xs font-semibold uppercase tracking-wider text-foreground-muted"
            >
              {day}
            </div>
          ))}
        </div>

        <div className="grid grid-cols-7">
          {Array.from({ length: startDay }).map((_, i) => (
            <div key={`empty-${i}`} className="min-h-[100px] border-b border-r border-border/50 bg-surface-secondary/30" />
          ))}

          {Array.from({ length: daysInMonth }).map((_, i) => {
            const day = i + 1
            const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`
            const dayEvents = eventsByDate.get(dateStr) ?? []
            const hasEvents = dayEvents.length > 0
            const isSelected = selectedDate === dateStr
            const todayHighlight = isToday(day)

            return (
              <motion.button
                key={day}
                whileTap={{ scale: 0.97 }}
                onClick={() => handleDayClick(day)}
                className={`relative min-h-[100px] border-b border-r border-border/50 p-2 text-left transition-all ${
                  isSelected
                    ? "bg-primary-50 shadow-inner"
                    : todayHighlight
                      ? "bg-blue-50/70"
                      : "hover:bg-surface-tertiary"
                }`}
              >
                <span
                  className={`mb-1 inline-flex h-7 w-7 items-center justify-center rounded-full text-sm font-semibold ${
                    todayHighlight
                      ? "bg-primary-600 text-white shadow-sm"
                      : "text-foreground"
                  }`}
                >
                  {day}
                </span>
                {hasEvents && (
                  <div className="mt-1 space-y-1">
                    {dayEvents.slice(0, 3).map((ev) => (
                      <div
                        key={ev.id}
                        className={`h-2 rounded-full ${getCategoryMarker(ev.category.name)}`}
                        title={ev.title}
                      />
                    ))}
                    {dayEvents.length > 3 && (
                      <span className="block text-[10px] font-medium text-foreground-muted">
                        +{dayEvents.length - 3}
                      </span>
                    )}
                  </div>
                )}
              </motion.button>
            )
          })}
        </div>
      </div>

      <AnimatePresence>
        {selectedDate && selectedEvents.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mt-5 overflow-hidden rounded-2xl border border-border bg-white p-5 shadow-sm"
          >
            <h3 className="mb-4 text-sm font-semibold text-foreground">
              Мероприятия {new Date(selectedDate + "T00:00:00").toLocaleDateString("ru-RU", {
                day: "numeric",
                month: "long",
                year: "numeric",
              })}
            </h3>
            <div className="space-y-3">
              {selectedEvents.map((ev) => (
                <Link
                  key={ev.id}
                  href={`/events/${ev.id}`}
                  className="group flex items-start gap-4 rounded-xl border border-border p-4 transition-all hover:border-primary-200 hover:shadow-sm"
                >
                  <div
                    className={`mt-1 h-3 w-3 shrink-0 rounded-full ${getCategoryMarker(ev.category.name)}`}
                  />
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-semibold text-foreground group-hover:text-primary-600 transition-colors">
                      {ev.title}
                    </p>
                    <div className="mt-1 flex flex-wrap gap-x-4 gap-y-1 text-xs text-foreground-muted">
                      {formatTime(ev.start_time) && (
                        <span className="flex items-center gap-1">
                          <Clock className="h-3 w-3" />
                          {formatTime(ev.start_time)}
                        </span>
                      )}
                      <span className="flex items-center gap-1">
                        <MapPin className="h-3 w-3" />
                        {ev.location}
                      </span>
                    </div>
                  </div>
                  <Badge className={getCategoryColors(ev.category.name)}>
                    {ev.category.name}
                  </Badge>
                </Link>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
