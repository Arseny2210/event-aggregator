"use client"

import { useState } from "react"
import Link from "next/link"
import { PageTransition } from "@/components/motion/PageTransition"
import { Plus } from "lucide-react"
import { Button } from "@/components/ui/Button"
import { EventList } from "@/components/features/events/EventList"
import {
  EventFilters,
  type EventFiltersValues,
} from "@/components/features/events/EventFilters"
import { useAuth } from "@/lib/hooks/useAuth"
import type { EventSearchParams } from "@/types/events"

export default function EventsPage() {
  const { user } = useAuth()
  const canManage = user?.permissions?.includes("event:manage")
  const [params, setParams] = useState<EventSearchParams>({
    limit: 20,
    offset: 0,
    sort: "date",
  })
  const [filters, setFilters] = useState<EventFiltersValues>({
    search: "",
    status: "",
    sort: "date",
  })

  const mergedParams: EventSearchParams = {
    ...params,
    search: filters.search || undefined,
    status: (filters.status || undefined) as EventSearchParams["status"],
    sort: filters.sort,
  }

  const handleFiltersChange = (values: EventFiltersValues) => {
    setFilters(values)
    setParams((p) => ({ ...p, offset: 0 }))
  }

  const handleClearFilters = () => {
    setFilters({ search: "", status: "", sort: "date" })
    setParams({ limit: 20, offset: 0, sort: "date" })
  }

  const handlePageChange = (offset: number) => {
    setParams((p) => ({ ...p, offset }))
  }

  return (
    <PageTransition>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground">
              Мероприятия
            </h1>
            <p className="text-sm text-foreground-secondary">
              Управление мероприятиями университета
            </p>
          </div>
          {canManage && (
            <Link href="/dashboard/events/new">
              <Button>
                <Plus className="mr-1 h-4 w-4" />
                Создать
              </Button>
            </Link>
          )}
        </div>

        <EventFilters
          values={filters}
          onChange={handleFiltersChange}
          onClear={handleClearFilters}
        />

        <EventList
          params={mergedParams}
          onPageChange={handlePageChange}
        />
      </div>
    </PageTransition>
  )
}
