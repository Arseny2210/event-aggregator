"use client"

import Link from "next/link"
import { Eye, Pencil, Trash2 } from "lucide-react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/Table"
import { Badge } from "@/components/ui/Badge"
import { Pagination } from "@/components/ui/Pagination"
import { Spinner } from "@/components/ui/Spinner"
import { Alert } from "@/components/ui/Alert"
import { Button } from "@/components/ui/Button"
import { useAuth } from "@/lib/hooks/useAuth"
import { useEvents } from "@/lib/hooks/useEvents"
import type { EventSearchParams } from "@/types/events"
import { EVENT_STATUS_COLORS, EVENT_STATUS_LABELS } from "@/types/events"

interface EventListProps {
  params: EventSearchParams
  onPageChange: (offset: number) => void
}

export function EventList({ params, onPageChange }: EventListProps) {
  const { user } = useAuth()
  const { data, isLoading, error } = useEvents(params)
  const canManage = user?.permissions?.includes("event:manage")

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Spinner className="h-8 w-8" />
      </div>
    )
  }

  if (error) {
    return <Alert variant="error">Failed to load events: {error.message}</Alert>
  }

  if (!data || data.items.length === 0) {
    return (
      <div className="py-12 text-center">
        <p className="text-slate-500">No events found.</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <Table>
        <TableHead>
          <TableRow>
            <TableHeader>Title</TableHeader>
            <TableHeader>Date</TableHeader>
            <TableHeader>Location</TableHeader>
            <TableHeader>Status</TableHeader>
            <TableHeader className="w-24">Actions</TableHeader>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.items.map((event) => (
            <TableRow key={event.id}>
              <TableCell className="font-medium">{event.title}</TableCell>
              <TableCell>{event.start_date}</TableCell>
              <TableCell>{event.location}</TableCell>
              <TableCell>
                <Badge className={EVENT_STATUS_COLORS[event.status]}>
                  {EVENT_STATUS_LABELS[event.status]}
                </Badge>
              </TableCell>
              <TableCell>
                <div className="flex gap-1">
                  <Link href={`/dashboard/events/${event.id}`}>
                    <Button variant="ghost" size="sm" aria-label="View event">
                      <Eye className="h-4 w-4" />
                    </Button>
                  </Link>
                  {canManage && (
                    <>
                      <Link href={`/dashboard/events/${event.id}/edit`}>
                        <Button variant="ghost" size="sm" aria-label="Edit event">
                          <Pencil className="h-4 w-4" />
                        </Button>
                      </Link>
                    </>
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
        onPrevious={() => onPageChange(Math.max(0, (params.offset || 0) - (params.limit || 20)))}
        onNext={() => onPageChange((params.offset || 0) + (params.limit || 20))}
      />
    </div>
  )
}
