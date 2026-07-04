import { apiClient } from "@/lib/api/client"
import { getAccessToken } from "@/lib/utils/auth"
import { API_URL } from "@/config"
import type { Page } from "@/types/api"
import type { ImportJob, ImportListParams, RowResult, RowResultParams } from "@/types/imports"

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

export const importsApi = {
  list: (params?: ImportListParams) =>
    apiClient.get<Page<ImportJob>>(`/imports${buildQuery(params as unknown as Record<string, unknown>)}`),

  getById: (id: string) =>
    apiClient.get<ImportJob>(`/imports/${id}`),

  getRows: (id: string, params?: RowResultParams) =>
    apiClient.get<Page<RowResult>>(`/imports/${id}/rows${buildQuery(params as unknown as Record<string, unknown>)}`),

  upload: async (file: File): Promise<ImportJob> => {
    const formData = new FormData()
    formData.append("file", file)
    const token = getAccessToken()
    const headers: Record<string, string> = {}
    if (token) headers["Authorization"] = `Bearer ${token}`
    const res = await fetch(`${API_URL}/imports`, {
      method: "POST",
      headers,
      body: formData,
    })
    if (!res.ok) {
      const body = await res.json().catch(() => ({}))
      throw new Error(body.detail || body.message || "Upload failed")
    }
    return res.json()
  },

  delete: (id: string) =>
    apiClient.delete<void>(`/imports/${id}`),
}
