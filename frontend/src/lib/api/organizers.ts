import { apiClient } from "@/lib/api/client"
import type { Organizer } from "@/types/organizers"

export const organizersApi = {
  list: () => apiClient.get<{ items: Organizer[]; total: number }>("/organizers"),
}
