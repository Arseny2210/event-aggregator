export interface ApiError {
  code: string
  message: string
}

export interface ApiErrorResponse {
  detail?: string
  error?: ApiError
  message?: string
}

export interface Page<T> {
  items: T[]
  total: number
  offset: number
  limit: number
}

export type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: string }
