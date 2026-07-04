import { apiClient } from "@/lib/api/client"
import type { Page } from "@/types/api"
import type {
  CreateEventDto,
  Event,
  EventSearchParams,
  UpdateEventDto,
} from "@/types/events"

function buildQuery(params?: EventSearchParams): string {
  if (!params) return ""
  const searchParams = new URLSearchParams()
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== "") {
      searchParams.set(key, String(value))
    }
  }
  const qs = searchParams.toString()
  return qs ? `?${qs}` : ""
}

export const eventsApi = {
  list: (params?: EventSearchParams) =>
    apiClient.get<Page<Event>>(`/events${buildQuery(params)}`),

  getById: (id: string) =>
    apiClient.get<Event>(`/events/${id}`),

  create: (data: CreateEventDto) =>
    apiClient.post<Event>("/events", data),

  update: (id: string, data: UpdateEventDto) =>
    apiClient.patch<Event>(`/events/${id}`, data),

  delete: (id: string) =>
    apiClient.delete<void>(`/events/${id}`),
}
