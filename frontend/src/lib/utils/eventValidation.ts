import { z } from "zod"

export const eventSchema = z.object({
  title: z.string().min(1, "Название обязательно").max(255),
  short_description: z.string().max(1000).optional().or(z.literal("")),
  description: z.string().min(1, "Описание обязательно").max(10000),
  start_date: z.string().min(1, "Дата обязательна").regex(/^\d{4}-\d{2}-\d{2}$/, "Используйте ГГГГ-ММ-ДД"),
  start_time: z.string().regex(/^\d{2}:\d{2}(:\d{2})?$/, "Используйте ЧЧ:ММ").optional().or(z.literal("")),
  end_time: z.string().regex(/^\d{2}:\d{2}(:\d{2})?$/, "Используйте ЧЧ:ММ").optional().or(z.literal("")),
  location: z.string().min(1, "Место обязательно").max(255),
  image_url: z.string().url("Должен быть валидный URL").max(2000).optional().or(z.literal("")),
  registration_url: z.string().url("Должен быть валидный URL").max(2000).optional().or(z.literal("")),
  status: z.enum(["draft", "published", "completed", "archived"]).optional(),
  organizer_id: z.string().uuid("Неверный UUID организатора"),
  category_id: z.string().uuid("Неверный UUID категории"),
  target_audience: z.string().max(100).optional().or(z.literal("")),
})

export type EventFormData = z.infer<typeof eventSchema>

export const eventUpdateSchema = eventSchema.partial()

export type EventUpdateFormData = z.infer<typeof eventUpdateSchema>
