import { apiClient } from "@/lib/api/client"
import type { LoginRequest, TokenResponse, UserMeResponse } from "@/types/auth"

export const authApi = {
  login: (data: LoginRequest) =>
    apiClient.post<TokenResponse>("/auth/login", data),

  refresh: (refreshToken: string) =>
    apiClient.post<TokenResponse>("/auth/refresh", {
      refresh_token: refreshToken,
    }),

  me: () => apiClient.get<UserMeResponse>("/auth/me"),

  logout: () => apiClient.post("/auth/logout"),
}
