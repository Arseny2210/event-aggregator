import { apiClient } from "@/lib/api/client"
import type { Page } from "@/types/api"
import type {
  NotifListParams,
  Notification,
  SendNotificationDto,
  SendTestNotificationDto,
} from "@/types/notifications"

function buildQuery(params?: Record<string, unknown>): string {
  if (!params) return ""
  const sp = new URLSearchParams()
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null && v !== "") {
      sp.set(k, String(v))
    }
  }
  const qs = sp.toString()
  return qs ? `?${qs}` : ""
}

export const notificationsApi = {
  list: (params?: NotifListParams) =>
    apiClient.get<Page<Notification>>(`/notifications${buildQuery(params as unknown as Record<string, unknown>)}`),

  getById: (id: string) =>
    apiClient.get<Notification>(`/notifications/${id}`),

  send: (data: SendNotificationDto) =>
    apiClient.post<Notification>("/notifications/send", data),

  sendTest: (data: SendTestNotificationDto) =>
    apiClient.post<Notification>("/notifications/test", data),

  listTemplates: (params?: { offset?: number; limit?: number }) =>
    apiClient.get<Page<unknown>>(`/notifications/templates${buildQuery(params as unknown as Record<string, unknown>)}`),
}
