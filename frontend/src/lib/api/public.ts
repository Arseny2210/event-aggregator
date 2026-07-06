import { apiClient } from "@/lib/api/client"
import type { Category } from "@/types/categories"
import type { Event } from "@/types/events"

export const publicApi = {
  categories: {
    list: () => apiClient.get<Category[]>("/categories"),
    create: (data: { name: string; description?: string | null }) =>
      apiClient.post<Category>("/categories/", data),
  },

  events: {
    list: (params?: { offset?: number; limit?: number; search?: string; status?: string; date_from?: string; date_to?: string }) => {
      const searchParams = new URLSearchParams()
      if (params) {
        for (const [key, value] of Object.entries(params)) {
          if (value !== undefined && value !== null && value !== "") {
            searchParams.set(key, String(value))
          }
        }
      }
      const qs = searchParams.toString()
      return apiClient.get<{ items: Event[]; total: number; offset: number; limit: number }>(`/events${qs ? `?${qs}` : ""}`)
    },

    getById: (id: string) => apiClient.get<Event>(`/events/${id}`),
  },

  participation: {
    register: (eventId: string) =>
      apiClient.post<{ id: string; event_id: string; session_id: string; status: string; created_at: string }>(
        `/events/${eventId}/participate`,
      ),

    cancel: (eventId: string) =>
      apiClient.delete<void>(`/events/${eventId}/participate`),

    status: (eventId: string) =>
      apiClient.get<{ is_registered: boolean }>(`/events/${eventId}/participate`),
  },
}
