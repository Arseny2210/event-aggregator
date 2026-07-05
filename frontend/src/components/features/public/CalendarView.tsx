"use client"

import { useState, useCallback, useMemo } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { ChevronLeft, ChevronRight, CalendarDays } from "lucide-react"
import { Button } from "@/components/ui/Button"
import { Badge } from "@/components/ui/Badge"
import { EventCard } from "./EventCard"
import type { Event } from "@/types/events"

interface CalendarViewProps {
  events: Event[]
}

const DAYS_OF_WEEK = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
const MONTHS = [
  "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
  "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь",
]

function getYearMonth(date: Date): string {
  return `${date.getFullYear()}-${String(date.getMonth()).padStart(2, "0")}`
}

function getDaysInMonth(year: number, month: number): number {
  return new Date(year, month + 1, 0).getDate()
}

function getStartDayOfWeek(year: number, month: number): number {
  const day = new Date(year, month, 1).getDay()
  return day === 0 ? 6 : day - 1
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

  const currentKey = `${currentYear}-${String(currentMonth + 1).padStart(2, "0")}`
  const daysInMonth = getDaysInMonth(currentYear, currentMonth)
  const startDay = getStartDayOfWeek(currentYear, currentMonth)

  const prevMonth = useCallback(() => {
    if (currentMonth === 0) {
      setCurrentYear((y: number) => y - 1)
      setCurrentMonth(11)
    } else {
      setCurrentMonth((m: number) => m - 1)
    }
    setSelectedDate(null)
    setSelectedEvents([])
  }, [currentMonth])

  const nextMonth = useCallback(() => {
    if (currentMonth === 11) {
      setCurrentYear((y: number) => y + 1)
      setCurrentMonth(0)
    } else {
      setCurrentMonth((m: number) => m + 1)
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

  const isToday = (day: number) => {
    return (
      currentYear === today.getFullYear() &&
      currentMonth === today.getMonth() &&
      day === today.getDate()
    )
  }

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <CalendarDays className="h-5 w-5 text-primary-600" />
          <h2 className="text-lg font-semibold text-foreground">
            {MONTHS[currentMonth]} {currentYear}
          </h2>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" onClick={goToToday}>
            Сегодня
          </Button>
          <Button variant="ghost" size="sm" onClick={prevMonth}>
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" onClick={nextMonth}>
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <div className="rounded-2xl border border-border bg-white p-4 shadow-sm">
        <div className="mb-2 grid grid-cols-7 gap-1">
          {DAYS_OF_WEEK.map((day) => (
            <div key={day} className="py-1 text-center text-xs font-medium text-foreground-muted">
              {day}
            </div>
          ))}
        </div>

        <div className="grid grid-cols-7 gap-1">
          {Array.from({ length: startDay }).map((_, i) => (
            <div key={`empty-${i}`} className="min-h-[80px] rounded-lg" />
          ))}

          {Array.from({ length: daysInMonth }).map((_, i) => {
            const day = i + 1
            const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`
            const dayEvents = eventsByDate.get(dateStr) ?? []
            const hasEvents = dayEvents.length > 0
            const isSelected = selectedDate === dateStr

            return (
              <motion.button
                key={day}
                whileTap={{ scale: 0.95 }}
                onClick={() => handleDayClick(day)}
                className={`relative min-h-[80px] rounded-lg border p-1.5 text-left text-sm transition-colors ${
                  isSelected
                    ? "border-primary-500 bg-primary-50"
                    : isToday(day)
                      ? "border-primary-300 bg-primary-50/50"
                      : "border-transparent hover:bg-surface-tertiary"
                }`}
              >
                <span
                  className={`inline-flex h-6 w-6 items-center justify-center rounded-full text-xs font-medium ${
                    isToday(day) ? "bg-primary-600 text-white" : "text-foreground"
                  }`}
                >
                  {day}
                </span>
                {hasEvents && (
                  <div className="mt-1 flex flex-wrap gap-0.5">
                    {dayEvents.slice(0, 3).map((ev) => (
                      <div
                        key={ev.id}
                        className="h-1.5 w-1.5 rounded-full bg-primary-500"
                        title={ev.title}
                      />
                    ))}
                    {dayEvents.length > 3 && (
                      <span className="text-[10px] text-foreground-muted">+{dayEvents.length - 3}</span>
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
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-4 overflow-hidden"
          >
            <h3 className="mb-3 text-sm font-medium text-foreground-secondary">
              Мероприятия на {selectedDate}
            </h3>
            <div className="space-y-3">
              {selectedEvents.map((ev) => (
                <EventCard key={ev.id} event={ev} />
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
