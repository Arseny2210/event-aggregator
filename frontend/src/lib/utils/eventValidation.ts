import { z } from "zod"

const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

const eventObjectSchema = z.object({
  title: z.string().min(1, "Название обязательно").max(255),
  short_description: z.string().max(1000).optional().or(z.literal("")),
  description: z.string().min(1, "Описание обязательно").max(10000),
  start_date: z
    .string()
    .min(1, "Дата обязательна")
    .regex(/^\d{4}-\d{2}-\d{2}$/, "Используйте ГГГГ-ММ-ДД"),
  start_time: z
    .string()
    .regex(/^\d{2}:\d{2}(:\d{2})?$/, "Используйте ЧЧ:ММ")
    .optional()
    .or(z.literal("")),
  end_time: z
    .string()
    .regex(/^\d{2}:\d{2}(:\d{2})?$/, "Используйте ЧЧ:ММ")
    .optional()
    .or(z.literal("")),
  location: z.string().min(1, "Место обязательно").max(255),
  image_url: z.string().max(2000).optional().or(z.literal("")),
  registration_url: z.string().max(2000).optional().or(z.literal("")),
  status: z.enum(["draft", "published", "completed", "archived"]).optional(),
  organizer_id: z
    .string()
    .min(1, "Организатор обязателен")
    .refine(
      (val) => UUID_REGEX.test(val),
      "Выберите организатора из списка",
    ),
  category_id: z
    .string()
    .min(1, "Категория обязательна")
    .refine(
      (val) => val === "__custom__" || UUID_REGEX.test(val),
      "Выберите категорию из списка",
    ),
  custom_category: z.string().max(100).optional().or(z.literal("")),
  target_audience: z.string().max(100).optional().or(z.literal("")),
  participation_enabled: z.boolean().optional(),
})

export const eventSchema = eventObjectSchema.refine(
  (data) => {
    if (data.category_id === "__custom__" && !data.custom_category) {
      return false
    }
    return true
  },
  {
    message: "Введите название категории",
    path: ["custom_category"],
  },
)

export type EventFormData = z.infer<typeof eventSchema>

export const eventUpdateSchema = eventObjectSchema.partial().refine(
  (data) => {
    if (data.category_id === "__custom__" && !data.custom_category) {
      return false
    }
    return true
  },
  {
    message: "Введите название категории",
    path: ["custom_category"],
  },
)

export type EventUpdateFormData = z.infer<typeof eventUpdateSchema>
