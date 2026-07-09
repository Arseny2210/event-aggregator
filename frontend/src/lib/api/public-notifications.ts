import { apiClient } from "@/lib/api/client"
import type { Page } from "@/types/api"
import type { Notification } from "@/types/notifications"

function buildQuery(params: Record<string, string | number>): string {
  const sp = new URLSearchParams()
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null && v !== "") {
      sp.set(k, String(v))
    }
  }
  const qs = sp.toString()
  return qs ? `?${qs}` : ""
}

export const publicNotificationsApi = {
  list: (sessionId: string, offset = 0, limit = 20) =>
    apiClient.get<Page<Notification>>(
      `/notifications/public${buildQuery({ session_id: sessionId, offset, limit })}`
    ),

  markAsRead: (notificationId: string, sessionId: string) =>
    apiClient.post<void>(
      `/notifications/${notificationId}/read${buildQuery({ session_id: sessionId })}`
    ),

  delete: (notificationId: string, sessionId: string) =>
    apiClient.delete<void>(
      `/notifications/${notificationId}${buildQuery({ session_id: sessionId })}`
    ),
}
