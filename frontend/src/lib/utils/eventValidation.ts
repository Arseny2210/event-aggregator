import { z } from "zod"

export const eventSchema = z.object({
  title: z.string().min(1, "Title is required").max(255),
  short_description: z.string().max(1000).optional().or(z.literal("")),
  description: z.string().min(1, "Description is required").max(10000),
  start_date: z.string().min(1, "Date is required").regex(/^\d{4}-\d{2}-\d{2}$/, "Use YYYY-MM-DD"),
  start_time: z.string().regex(/^\d{2}:\d{2}(:\d{2})?$/, "Use HH:MM").optional().or(z.literal("")),
  end_time: z.string().regex(/^\d{2}:\d{2}(:\d{2})?$/, "Use HH:MM").optional().or(z.literal("")),
  location: z.string().min(1, "Location is required").max(255),
  image_url: z.string().url("Must be a valid URL").max(2000).optional().or(z.literal("")),
  registration_url: z.string().url("Must be a valid URL").max(2000).optional().or(z.literal("")),
  status: z.enum(["draft", "published", "completed", "archived"]).optional(),
  organizer_id: z.string().uuid("Invalid organizer ID"),
  category_id: z.string().uuid("Invalid category ID"),
})

export type EventFormData = z.infer<typeof eventSchema>

export const eventUpdateSchema = eventSchema.partial()

export type EventUpdateFormData = z.infer<typeof eventUpdateSchema>
