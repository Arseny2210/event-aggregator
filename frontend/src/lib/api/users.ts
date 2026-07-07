import { apiClient } from "@/lib/api/client"
import type { Page } from "@/types/api"

export interface UserInfo {
  id: string
  username: string
  email: string
  role: { id: number; name: string }
  is_active: boolean
}

export const usersApi = {
  list: (params?: { offset?: number; limit?: number }) =>
    apiClient.get<Page<UserInfo>>(
      `/users${params ? `?${new URLSearchParams(Object.entries(params).map(([k, v]) => [k, String(v)])).toString()}` : ""}`,
    ),

  create: (data: { username: string; email: string; password: string; role_name: string }) =>
    apiClient.post<UserInfo>("/users", data),

  changeRole: (userId: string, roleName: string) =>
    apiClient.patch<UserInfo>(`/users/${userId}/role`, { role_name: roleName }),
}
