"use client"

import { useState, useMemo } from "react"
import Link from "next/link"
import { motion, AnimatePresence } from "framer-motion"
import Image from "next/image"
import { Eye, Pencil, Calendar, MapPin, Check, X, AlertTriangle } from "lucide-react"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/Table"
import { Badge } from "@/components/ui/Badge"
import { Pagination } from "@/components/ui/Pagination"
import { Spinner } from "@/components/ui/Spinner"
import { Alert } from "@/components/ui/Alert"
import { Button } from "@/components/ui/Button"
import { Checkbox } from "@/components/ui/Checkbox"
import { useAuth } from "@/lib/hooks/useAuth"
import { useEvents, useBatchEventStatus } from "@/lib/hooks/useEvents"
import { EmptyState } from "@/components/layout/EmptyState"
import type { EventSearchParams } from "@/types/events"
import { EVENT_STATUS_COLORS, EVENT_STATUS_LABELS } from "@/types/events"
import { getCategoryColors } from "@/types/categories"
import { getImageUrl } from "@/config"

interface EventListProps {
  params: EventSearchParams
  onPageChange: (offset: number) => void
}

export function EventList({ params, onPageChange }: EventListProps) {
  const { user } = useAuth()
  const { data, isLoading, error } = useEvents(params)
  const batch = useBatchEventStatus()
  const canManage = user?.permissions?.includes("event:manage")

  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set())

  const [batchError, setBatchError] = useState<string | null>(null)

  const allIds = useMemo(
    () => new Set((data?.items ?? []).map((e) => e.id)),
    [data],
  )

  const allSelected =
    allIds.size > 0 && selectedIds.size === allIds.size

  const toggleAll = () => {
    if (allSelected) {
      setSelectedIds(new Set())
    } else {
      setSelectedIds(new Set(allIds))
    }
  }

  const toggleOne = (id: string) => {
    setSelectedIds((prev) => {
      const next = new Set(prev)
      if (next.has(id)) {
        next.delete(id)
      } else {
        next.add(id)
      }
      return next
    })
  }

  const handleBatchStatus = async (status: string) => {
    if (selectedIds.size === 0) return
    setBatchError(null)
    try {
      const result = await batch.mutateAsync({
        eventIds: Array.from(selectedIds),
        status,
      })
      if (result.errors.length > 0) {
        setBatchError(
          `Успешно: ${result.success}. Ошибок: ${result.errors.length} (${result.errors.slice(0, 3).map((e: { event_id: string }) => e.event_id.slice(0, 8)).join(", ")}...)`,
        )
      } else {
        setSelectedIds(new Set())
      }
    } catch {
      setBatchError("Не удалось выполнить операцию")
    }
  }

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
        Ошибка загрузки мероприятий: {error.message}
      </Alert>
    )
  }

  if (!data || data.items.length === 0) {
    return (
      <EmptyState
        title="Мероприятия не найдены"
        description="Попробуйте изменить параметры поиска"
      />
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-4"
    >
      {canManage && selectedIds.size > 0 && (
        <>
          {batchError && (
            <motion.div
              initial={{ opacity: 0, y: -5 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex items-center gap-2 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700"
            >
              <AlertTriangle className="h-4 w-4 shrink-0" />
              {batchError}
              <button
                onClick={() => setBatchError(null)}
                className="ml-auto text-red-400 hover:text-red-600"
              >
                <X className="h-4 w-4" />
              </button>
            </motion.div>
          )}
          <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-2 rounded-xl border border-primary-200 bg-primary-50 p-3"
        >
          <span className="text-sm font-medium text-primary-700">
            Выбрано: {selectedIds.size}
          </span>
          <div className="ml-auto flex gap-2">
            <Button
              size="sm"
              variant="secondary"
              onClick={() => handleBatchStatus("draft")}
              isLoading={batch.isPending}
            >
              В черновик
            </Button>
            <Button
              size="sm"
              variant="primary"
              onClick={() => handleBatchStatus("published")}
              isLoading={batch.isPending}
            >
              Опубликовать
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => setSelectedIds(new Set())}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </motion.div>
        </>
      )}

      <Table>
        <TableHead>
          <TableRow>
            {canManage && (
              <TableHeader className="w-10">
                <Checkbox
                  checked={allSelected}
                  onChange={toggleAll}
                  aria-label="Выбрать все"
                />
              </TableHeader>
            )}
            <TableHeader>Название</TableHeader>
            <TableHeader>Дата</TableHeader>
            <TableHeader>Место</TableHeader>
            <TableHeader>Категория</TableHeader>
            <TableHeader>Статус</TableHeader>
            <TableHeader className="w-24">Действия</TableHeader>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.items.map((event) => (
            <TableRow key={event.id}>
              {canManage && (
                <TableCell>
                  <Checkbox
                    checked={selectedIds.has(event.id)}
                    onChange={() => toggleOne(event.id)}
                    aria-label={`Выбрать ${event.title}`}
                  />
                </TableCell>
              )}
              <TableCell>
                <div className="flex items-center gap-3">
                  {event.image_url ? (
                    <Image
                      src={getImageUrl(event.image_url)}
                      alt=""
                      width={40}
                      height={40}
                      className="h-10 w-10 rounded-lg object-cover"
                    />
                  ) : (
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary-50 text-primary-600 text-xs font-bold">
                      {event.title.charAt(0)}
                    </div>
                  )}
                  <div>
                    <p className="font-medium text-foreground">{event.title}</p>
                    {event.target_audience && (
                      <p className="text-xs text-foreground-muted">{event.target_audience}</p>
                    )}
                  </div>
                </div>
              </TableCell>
              <TableCell>
                <span className="flex items-center gap-1 text-sm">
                  <Calendar className="h-3.5 w-3.5 text-foreground-muted" />
                  {new Date(event.start_date).toLocaleDateString("ru-RU")}
                  {event.start_time ? ` ${event.start_time}` : ""}
                </span>
              </TableCell>
              <TableCell>
                <span className="flex items-center gap-1 text-sm">
                  <MapPin className="h-3.5 w-3.5 text-foreground-muted" />
                  {event.location}
                </span>
              </TableCell>
              <TableCell>
                {event.category && (
                  <Badge className={getCategoryColors(event.category.name)}>
                    {event.category.name}
                  </Badge>
                )}
              </TableCell>
              <TableCell>
                <Badge className={EVENT_STATUS_COLORS[event.status]}>
                  {EVENT_STATUS_LABELS[event.status]}
                </Badge>
              </TableCell>
              <TableCell>
                <div className="flex gap-1">
                  <Link href={`/dashboard/events/${event.id}`}>
                    <Button variant="ghost" size="sm" aria-label="Просмотр">
                      <Eye className="h-4 w-4" />
                    </Button>
                  </Link>
                  {canManage && (
                    <Link href={`/dashboard/events/${event.id}/edit`}>
                      <Button
                        variant="ghost"
                        size="sm"
                        aria-label="Редактировать"
                      >
                        <Pencil className="h-4 w-4" />
                      </Button>
                    </Link>
                  )}
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <Pagination
        offset={data.offset}
        limit={data.limit}
        total={data.total}
        onPrevious={() =>
          onPageChange(
            Math.max(0, (params.offset || 0) - (params.limit || 20)),
          )
        }
        onNext={() =>
          onPageChange((params.offset || 0) + (params.limit || 20))
        }
      />
    </motion.div>
  )
}
