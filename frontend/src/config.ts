export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"
export const APP_NAME = "ИС «Мероприятия»"

const BASE_URL = API_URL.replace(/\/api\/v1$/, "")

export function getImageUrl(path: string | null | undefined): string {
  if (!path) return ""
  if (path.startsWith("http") || path.startsWith("data:")) return path
  if (path.startsWith("/")) return `${BASE_URL}${path}`
  return `${BASE_URL}/${path}`
}
