"use client"

import { useEffect, useRef } from "react"
import { Input } from "@/components/ui/Input"
import { Select } from "@/components/ui/Select"
import { Button } from "@/components/ui/Button"
import { type EventStatus } from "@/types/events"

export interface EventFiltersValues {
  search: string
  status: string
  sort: string
}

interface EventFiltersProps {
  values: EventFiltersValues
  onChange: (values: EventFiltersValues) => void
  onClear: () => void
}

const STATUS_OPTIONS = [
  { value: "", label: "All statuses" },
  { value: "draft", label: "Draft" },
  { value: "published", label: "Published" },
  { value: "completed", label: "Completed" },
  { value: "archived", label: "Archived" },
]

const SORT_OPTIONS = [
  { value: "date", label: "Date (ascending)" },
  { value: "-date", label: "Date (descending)" },
  { value: "title", label: "Title (A-Z)" },
  { value: "-title", label: "Title (Z-A)" },
  { value: "created_at", label: "Created (ascending)" },
  { value: "-created_at", label: "Created (descending)" },
]

export function EventFilters({ values, onChange, onClear }: EventFiltersProps) {
  const searchTimerRef = useRef<NodeJS.Timeout | null>(null)

  const handleSearchInput = (search: string) => {
    if (searchTimerRef.current) clearTimeout(searchTimerRef.current)
    searchTimerRef.current = setTimeout(() => {
      onChange({ ...values, search })
    }, 300)
  }

  useEffect(() => {
    return () => {
      if (searchTimerRef.current) clearTimeout(searchTimerRef.current)
    }
  }, [])

  const hasFilters = values.search || values.status || values.sort !== "date"

  return (
    <div className="flex flex-wrap items-end gap-3">
      <div className="min-w-[200px] flex-1">
        <Input
          placeholder="Search events..."
          defaultValue={values.search}
          onChange={(e) => handleSearchInput(e.target.value)}
        />
      </div>
      <div className="w-40">
        <Select
          options={STATUS_OPTIONS}
          value={values.status}
          onChange={(e) => onChange({ ...values, status: e.target.value })}
        />
      </div>
      <div className="w-52">
        <Select
          options={SORT_OPTIONS}
          value={values.sort}
          onChange={(e) => onChange({ ...values, sort: e.target.value })}
        />
      </div>
      {hasFilters && (
        <Button variant="ghost" size="sm" onClick={onClear}>
          Clear
        </Button>
      )}
    </div>
  )
}
