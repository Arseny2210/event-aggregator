"use client"

import { useEffect, useRef } from "react"
import { Input } from "@/components/ui/Input"
import { Select } from "@/components/ui/Select"
import { Button } from "@/components/ui/Button"

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
  { value: "", label: "Все статусы" },
  { value: "draft", label: "Черновик" },
  { value: "published", label: "Опубликовано" },
  { value: "completed", label: "Завершено" },
  { value: "archived", label: "В архиве" },
]

const SORT_OPTIONS = [
  { value: "date", label: "Дата (возрастание)" },
  { value: "-date", label: "Дата (убывание)" },
  { value: "title", label: "Название (А-Я)" },
  { value: "-title", label: "Название (Я-А)" },
  { value: "created_at", label: "Создан (возрастание)" },
  { value: "-created_at", label: "Создан (убывание)" },
]

export function EventFilters({
  values,
  onChange,
  onClear,
}: EventFiltersProps) {
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

  const hasFilters =
    values.search || values.status || values.sort !== "date"

  return (
    <div className="flex flex-wrap items-end gap-3">
      <div className="min-w-[200px] flex-1">
        <Input
          placeholder="Поиск мероприятий..."
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
          Сбросить
        </Button>
      )}
    </div>
  )
}
