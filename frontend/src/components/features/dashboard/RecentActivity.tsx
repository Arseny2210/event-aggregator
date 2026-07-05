"use client"

import { Card, CardHeader, CardTitle } from "@/components/ui/Card"
import { Badge } from "@/components/ui/Badge"
import { Skeleton } from "@/components/ui/Skeleton"
import { Clock } from "lucide-react"
import { useEvents } from "@/lib/hooks/useEvents"
import { EVENT_STATUS_LABELS, EVENT_STATUS_COLORS } from "@/types/events"

export function RecentActivity() {
  const { data, isLoading } = useEvents({ limit: 5 })

  return (
    <Card>
      <CardHeader>
        <CardTitle>Последние мероприятия</CardTitle>
      </CardHeader>
      <div className="space-y-3">
        {isLoading ? (
          <>
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="flex items-center gap-3">
                <Skeleton className="h-2 w-2 rounded-full" />
                <div className="flex-1">
                  <Skeleton className="mb-1 h-4 w-3/4" />
                  <Skeleton className="h-3 w-1/2" />
                </div>
              </div>
            ))}
          </>
        ) : data?.items.length === 0 ? (
          <p className="py-6 text-center text-sm text-foreground-muted">
            Нет мероприятий
          </p>
        ) : (
          data?.items.map((event) => (
            <div
              key={event.id}
              className="flex items-center gap-3 rounded-xl border border-border p-3 transition-colors hover:bg-surface-secondary"
            >
              <div className="flex-shrink-0">
                <Clock className="h-4 w-4 text-foreground-muted" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium text-foreground">
                  {event.title}
                </p>
                <p className="text-xs text-foreground-muted">
                  {new Date(event.start_date).toLocaleDateString("ru-RU")}
                </p>
              </div>
              <Badge className={EVENT_STATUS_COLORS[event.status]}>
                {EVENT_STATUS_LABELS[event.status]}
              </Badge>
            </div>
          ))
        )}
      </div>
    </Card>
  )
}
