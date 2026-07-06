export interface Category {
  id: string
  name: string
  description?: string | null
}

export const DEFAULT_CATEGORIES = [
  "Лекция",
  "Хакатон",
  "Спорт",
  "Конкурс",
  "Карьера",
  "Культура",
  "Другая",
]

const CATEGORY_COLORS_MAP: Record<string, string> = {
  "Лекция": "bg-blue-100 text-blue-700 border-blue-200",
  "Хакатон": "bg-purple-100 text-purple-700 border-purple-200",
  "Спорт": "bg-green-100 text-green-700 border-green-200",
  "Конкурс": "bg-orange-100 text-orange-700 border-orange-200",
  "Карьера": "bg-indigo-100 text-indigo-700 border-indigo-200",
  "Культура": "bg-pink-100 text-pink-700 border-pink-200",
  "Другая": "bg-gray-100 text-gray-700 border-gray-200",
}

const CATEGORY_MARKER_MAP: Record<string, string> = {
  "Лекция": "bg-blue-500",
  "Хакатон": "bg-purple-500",
  "Спорт": "bg-green-500",
  "Конкурс": "bg-orange-500",
  "Карьера": "bg-indigo-500",
  "Культура": "bg-pink-500",
  "Другая": "bg-gray-500",
}

export function getCategoryColors(name: string): string {
  return CATEGORY_COLORS_MAP[name] ?? "bg-gray-100 text-gray-700 border-gray-200"
}

export function getCategoryMarker(name: string): string {
  return CATEGORY_MARKER_MAP[name] ?? "bg-gray-500"
}
