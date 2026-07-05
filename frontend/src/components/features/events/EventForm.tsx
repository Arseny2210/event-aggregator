"use client"

import { useMemo } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { useRouter } from "next/navigation"
import { motion } from "framer-motion"
import { Input } from "@/components/ui/Input"
import { Textarea } from "@/components/ui/Textarea"
import { Select } from "@/components/ui/Select"
import { Button } from "@/components/ui/Button"
import { Card, CardHeader, CardTitle } from "@/components/ui/Card"
import { Alert } from "@/components/ui/Alert"
import { eventSchema, type EventFormData } from "@/lib/utils/eventValidation"
import { useCreateEvent, useUpdateEvent } from "@/lib/hooks/useEvents"
import { useCategories } from "@/lib/hooks/usePublic"
import { type Event } from "@/types/events"

interface EventFormProps {
  event?: Event
  isEditing?: boolean
}

const STATUS_OPTIONS = [
  { value: "draft", label: "Черновик" },
  { value: "published", label: "Опубликовано" },
  { value: "completed", label: "Завершено" },
  { value: "archived", label: "В архиве" },
]

const TARGET_AUDIENCE_OPTIONS = [
  { value: "Все желающие", label: "Все желающие" },
  { value: "Студенты", label: "Студенты" },
  { value: "Преподаватели", label: "Преподаватели" },
  { value: "1–2 курс", label: "1–2 курс" },
  { value: "3–4 курс", label: "3–4 курс" },
  { value: "Магистранты", label: "Магистранты" },
]

export function EventForm({ event, isEditing }: EventFormProps) {
  const router = useRouter()
  const createEvent = useCreateEvent()
  const updateEvent = useUpdateEvent()
  const { data: categories = [] } = useCategories()

  const categoryOptions = useMemo(
    () => categories.map((c) => ({ value: c.id, label: c.name })),
    [categories],
  )

  const defaultValues: EventFormData = event
    ? {
        title: event.title,
        short_description: event.short_description || "",
        description: event.description,
        start_date: event.start_date,
        start_time: event.start_time || "",
        end_time: event.end_time || "",
        location: event.location,
        image_url: event.image_url || "",
        registration_url: event.registration_url || "",
        status: event.status,
        organizer_id: event.organizer_id,
        category_id: event.category_id,
        target_audience: event.target_audience || "",
      }
    : {
        title: "",
        short_description: "",
        description: "",
        start_date: "",
        start_time: "",
        end_time: "",
        location: "",
        image_url: "",
        registration_url: "",
        status: "draft",
        organizer_id: "",
        category_id: "",
        target_audience: "",
      }

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<EventFormData>({
    resolver: zodResolver(eventSchema),
    defaultValues,
  })

  const error = createEvent.error || updateEvent.error

  const onSubmit = async (data: EventFormData) => {
    const payload = {
      ...data,
      short_description: data.short_description || undefined,
      start_time: data.start_time || undefined,
      end_time: data.end_time || undefined,
      image_url: data.image_url || undefined,
      registration_url: data.registration_url || undefined,
      target_audience: data.target_audience || undefined,
    }

    if (isEditing && event) {
      await updateEvent.mutateAsync({ id: event.id, data: payload })
      router.push(`/dashboard/events/${event.id}`)
    } else {
      const result = await createEvent.mutateAsync(payload)
      router.push(`/dashboard/events/${result.id}`)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          {isEditing
            ? "Редактирование мероприятия"
            : "Создание мероприятия"}
        </CardTitle>
      </CardHeader>
      <motion.form
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        onSubmit={handleSubmit(onSubmit)}
        className="space-y-4"
      >
        {error && <Alert variant="error">{error.message}</Alert>}

        <Input
          label="Название"
          placeholder="Название мероприятия"
          {...register("title")}
          error={errors.title?.message}
        />

        <Textarea
          label="Описание"
          rows={4}
          placeholder="Полное описание мероприятия"
          {...register("description")}
          error={errors.description?.message}
        />

        <div className="grid gap-4 sm:grid-cols-2">
          <Input
            label="Дата начала"
            type="date"
            {...register("start_date")}
            error={errors.start_date?.message}
          />
          <Input
            label="Время начала"
            type="time"
            {...register("start_time")}
            error={errors.start_time?.message}
          />
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <Input
            label="Время окончания"
            type="time"
            {...register("end_time")}
            error={errors.end_time?.message}
          />
          <Input
            label="Место проведения"
            placeholder="Адрес или аудитория"
            {...register("location")}
            error={errors.location?.message}
          />
        </div>

        <Input
          label="Краткое описание"
          placeholder="Краткий анонс (необязательно)"
          {...register("short_description")}
          error={errors.short_description?.message}
        />

        <div className="grid gap-4 sm:grid-cols-2">
          <Input
            label="URL изображения"
            type="url"
            placeholder="https://example.com/image.jpg"
            {...register("image_url")}
            error={errors.image_url?.message}
          />
          <Input
            label="URL регистрации"
            type="url"
            placeholder="https://example.com/register"
            {...register("registration_url")}
            error={errors.registration_url?.message}
          />
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <Select
            label="Категория"
            options={categoryOptions}
            {...register("category_id")}
            error={errors.category_id?.message}
          />
          <Select
            label="Целевая аудитория"
            options={TARGET_AUDIENCE_OPTIONS}
            {...register("target_audience")}
            error={errors.target_audience?.message}
          />
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          <Select
            label="Статус"
            options={STATUS_OPTIONS}
            {...register("status")}
            error={errors.status?.message}
          />
          <Input
            label="ID организатора"
            placeholder="UUID"
            {...register("organizer_id")}
            error={errors.organizer_id?.message}
          />
        </div>

        <div className="flex gap-3 pt-2">
          <Button type="submit" isLoading={isSubmitting}>
            {isEditing ? "Сохранить изменения" : "Создать мероприятие"}
          </Button>
          <Button
            type="button"
            variant="secondary"
            onClick={() => router.back()}
          >
            Отмена
          </Button>
        </div>
      </motion.form>
    </Card>
  )
}
