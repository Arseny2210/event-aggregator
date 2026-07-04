"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { useRouter } from "next/navigation"
import { Input } from "@/components/ui/Input"
import { Select } from "@/components/ui/Select"
import { Button } from "@/components/ui/Button"
import { Card } from "@/components/ui/Card"
import { Alert } from "@/components/ui/Alert"
import { eventSchema, type EventFormData } from "@/lib/utils/eventValidation"
import { useCreateEvent, useUpdateEvent } from "@/lib/hooks/useEvents"
import { type Event } from "@/types/events"

interface EventFormProps {
  event?: Event
  isEditing?: boolean
}

const STATUS_OPTIONS = [
  { value: "draft", label: "Draft" },
  { value: "published", label: "Published" },
  { value: "completed", label: "Completed" },
  { value: "archived", label: "Archived" },
]

export function EventForm({ event, isEditing }: EventFormProps) {
  const router = useRouter()
  const createEvent = useCreateEvent()
  const updateEvent = useUpdateEvent()

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
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {error && <Alert variant="error">{error.message}</Alert>}

        <Input
          label="Title"
          placeholder="Event title"
          {...register("title")}
          error={errors.title?.message}
        />

        <div>
          <label className="mb-1 block text-sm font-medium text-slate-700">
            Description
          </label>
          <textarea
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 transition-colors focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            rows={4}
            placeholder="Event description"
            {...register("description")}
          />
          {errors.description && (
            <p className="mt-1 text-xs text-red-600">{errors.description.message}</p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <Input
            label="Start Date"
            type="date"
            {...register("start_date")}
            error={errors.start_date?.message}
          />
          <Input
            label="Start Time"
            type="time"
            {...register("start_time")}
            error={errors.start_time?.message}
          />
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <Input
            label="End Time"
            type="time"
            {...register("end_time")}
            error={errors.end_time?.message}
          />
          <Input
            label="Location"
            placeholder="Venue location"
            {...register("location")}
            error={errors.location?.message}
          />
        </div>

        <Input
          label="Short Description"
          type="text"
          placeholder="Brief summary (optional)"
          {...register("short_description")}
          error={errors.short_description?.message}
        />

        <div className="grid gap-4 sm:grid-cols-2">
          <Input
            label="Image URL"
            type="url"
            placeholder="https://example.com/image.jpg"
            {...register("image_url")}
            error={errors.image_url?.message}
          />
          <Input
            label="Registration URL"
            type="url"
            placeholder="https://example.com/register"
            {...register("registration_url")}
            error={errors.registration_url?.message}
          />
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          <Select
            label="Status"
            options={STATUS_OPTIONS}
            {...register("status")}
            error={errors.status?.message}
          />
          <Input
            label="Organizer ID"
            placeholder="UUID"
            {...register("organizer_id")}
            error={errors.organizer_id?.message}
          />
          <Input
            label="Category ID"
            placeholder="UUID"
            {...register("category_id")}
            error={errors.category_id?.message}
          />
        </div>

        <div className="flex gap-3 pt-2">
          <Button type="submit" isLoading={isSubmitting}>
            {isEditing ? "Update Event" : "Create Event"}
          </Button>
          <Button
            type="button"
            variant="secondary"
            onClick={() => router.back()}
          >
            Cancel
          </Button>
        </div>
      </form>
    </Card>
  )
}
