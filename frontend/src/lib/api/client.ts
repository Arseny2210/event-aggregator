import { API_URL } from "@/config"
import { clearTokens, getAccessToken, getRefreshToken, setTokens } from "@/lib/utils/auth"

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    const token = getAccessToken()

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...((options.headers as Record<string, string>) || {}),
    }

    if (token) {
      headers["Authorization"] = `Bearer ${token}`
    }

    const response = await fetch(url, {
      ...options,
      headers,
    })

    if (response.status === 401 && token) {
      const refreshed = await this.tryRefresh()
      if (refreshed) {
        headers["Authorization"] = `Bearer ${getAccessToken()}`
        const retryResponse = await fetch(url, { ...options, headers })
        if (!retryResponse.ok) {
          throw await this.parseError(retryResponse)
        }
        return retryResponse.json()
      }
      clearTokens()
      window.location.href = "/login"
      throw new Error("Session expired")
    }

    if (response.status === 204) {
      return undefined as T
    }

    if (!response.ok) {
      throw await this.parseError(response)
    }

    return response.json()
  }

  private async tryRefresh(): Promise<boolean> {
    const refreshToken = getRefreshToken()
    if (!refreshToken) return false

    try {
      const response = await fetch(`${this.baseUrl}/auth/refresh`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: refreshToken }),
      })

      if (!response.ok) return false

      const data = await response.json()
      setTokens(data.access_token, data.refresh_token)
      return true
    } catch {
      return false
    }
  }

  private async parseError(response: Response): Promise<Error> {
    try {
      const body = await response.json()
      const message =
        body.detail || body.error?.message || body.message || response.statusText
      return new Error(message)
    } catch {
      return new Error(response.statusText)
    }
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: "GET" })
  }

  async post<T>(endpoint: string, body?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: "POST",
      body: body ? JSON.stringify(body) : undefined,
    })
  }

  async patch<T>(endpoint: string, body?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: "PATCH",
      body: body ? JSON.stringify(body) : undefined,
    })
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: "DELETE" })
  }
}

export const apiClient = new ApiClient(API_URL)
