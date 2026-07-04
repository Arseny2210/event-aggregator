export type EventStatus = "draft" | "published" | "completed" | "archived"

export interface Event {
  id: string
  title: string
  short_description?: string
  description: string
  start_date: string
  start_time?: string
  end_time?: string
  location: string
  image_url?: string
  registration_url?: string
  status: EventStatus
  organizer_id: string
  category_id: string
  created_at: string
  updated_at: string
}

export interface EventSearchParams {
  offset?: number
  limit?: number
  search?: string
  status?: EventStatus
  organizer_id?: string
  organizer_name?: string
  category_id?: string
  date_from?: string
  date_to?: string
  sort?: string
}

export interface CreateEventDto {
  title: string
  short_description?: string
  description: string
  start_date: string
  start_time?: string
  end_time?: string
  location: string
  image_url?: string
  registration_url?: string
  status?: EventStatus
  organizer_id: string
  category_id: string
}

export type UpdateEventDto = Partial<CreateEventDto>

export const EVENT_STATUS_LABELS: Record<EventStatus, string> = {
  draft: "Draft",
  published: "Published",
  completed: "Completed",
  archived: "Archived",
}

export const EVENT_STATUS_COLORS: Record<EventStatus, string> = {
  draft: "bg-slate-100 text-slate-700",
  published: "bg-green-100 text-green-700",
  completed: "bg-blue-100 text-blue-700",
  archived: "bg-amber-100 text-amber-700",
}
