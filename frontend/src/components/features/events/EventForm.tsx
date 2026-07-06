"use client"

import { useMemo, useState, useRef, useCallback, useEffect } from "react"
import { useForm, Controller } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { useRouter } from "next/navigation"
import { motion } from "framer-motion"
import Image from "next/image"
import { Input } from "@/components/ui/Input"
import { Textarea } from "@/components/ui/Textarea"
import { Select } from "@/components/ui/Select"
import { Button } from "@/components/ui/Button"
import { Card, CardHeader, CardTitle } from "@/components/ui/Card"
import { Alert } from "@/components/ui/Alert"
import { eventSchema, type EventFormData } from "@/lib/utils/eventValidation"
import { useCreateEvent, useUpdateEvent } from "@/lib/hooks/useEvents"
import { useCategories } from "@/lib/hooks/usePublic"
import { useOrganizers } from "@/lib/hooks/useOrganizers"
import { useAuth } from "@/lib/hooks/useAuth"
import { type Event } from "@/types/events"
import { DEFAULT_CATEGORIES } from "@/types/categories"
import { ImagePlus, Trash2, Upload, Link, Info } from "lucide-react"
import { API_URL, getImageUrl } from "@/config"
import { apiClient } from "@/lib/api/client"
import { publicApi } from "@/lib/api/public"

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
  const { data: organizersData } = useOrganizers()
  const { user } = useAuth()

  const [imageFile, setImageFile] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string | null>(
    event?.image_url ?? null,
  )
  const [isUploading, setIsUploading] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const organizers = organizersData?.items ?? []
  const isAdmin = user?.role?.name === "admin"

  const categoryOptions = useMemo(() => {
    const fromApi = categories.map((c) => ({ value: c.id, label: c.name }))
    return [
      ...fromApi,
      { value: "__custom__", label: "Другая (указать вручную)" },
    ]
  }, [categories])

  const defaultCategoryId = useMemo(() => {
    if (!event) return ""
    return categories.find((c) => c.id === event.category_id)?.id ?? ""
  }, [event, categories])

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
        category_id: defaultCategoryId,
        custom_category: "",
        target_audience: event.target_audience || "",
        participation_enabled: event.participation_enabled,
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
        status: "draft" as const,
        organizer_id: organizers.length === 1 ? organizers[0].id : "",
        category_id: "",
        custom_category: "",
        target_audience: "",
        participation_enabled: true,
      }

const FORM_STORAGE_KEY = "event-form-draft"

  const {
    register,
    handleSubmit,
    control,
    watch,
    setValue,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<EventFormData>({
    resolver: zodResolver(eventSchema),
    defaultValues: (() => {
      if (event) return defaultValues
      try {
        const saved = localStorage.getItem(FORM_STORAGE_KEY)
        if (saved) {
          const parsed = JSON.parse(saved)
          return { ...defaultValues, ...parsed }
        }
      } catch {}
      return defaultValues
    })(),
  })

  const watchedValues = watch()

  useEffect(() => {
    if (isEditing) return
    const timeout = setTimeout(() => {
      localStorage.setItem(FORM_STORAGE_KEY, JSON.stringify(watchedValues))
    }, 300)
    return () => clearTimeout(timeout)
  }, [watchedValues, isEditing])

  useEffect(() => {
    if (!event) return
    if (categories.length === 0) return
    const correctId = categories.find((c) => c.id === event.category_id)?.id
    if (correctId) {
      setValue("category_id", correctId, { shouldValidate: false })
    }
  }, [categories, event, setValue])

  useEffect(() => {
    if (isEditing || event) return
    const orgs = organizersData?.items ?? []
    if (orgs.length === 1) {
      setValue("organizer_id", orgs[0].id, { shouldValidate: false })
    }
  }, [organizersData, event, isEditing, setValue])

  const error = createEvent.error || updateEvent.error
  const selectedCategoryId = watch("category_id")
  const isCustomCategory = selectedCategoryId === "__custom__"

  const handleImageSelected = useCallback(async (file: File) => {
    if (!file.type.startsWith("image/")) return
    if (file.size > 10 * 1024 * 1024) return

    setImageFile(file)
    const reader = new FileReader()
    reader.onload = (e) => setImagePreview(e.target?.result as string)
    reader.readAsDataURL(file)
  }, [])

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      const file = e.dataTransfer.files[0]
      if (file) handleImageSelected(file)
    },
    [handleImageSelected],
  )

  const removeImage = useCallback(() => {
    setImageFile(null)
    setImagePreview(null)
    setValue("image_url", "")
    if (fileInputRef.current) fileInputRef.current.value = ""
  }, [setValue])

  const onSubmit = async (data: EventFormData) => {
    let imageUrl = data.image_url || ""

    if (imageFile) {
      setIsUploading(true)
      try {
        const formData = new FormData()
        formData.append("file", imageFile)
        const resp = await fetch(`${API_URL}/upload/image`, {
          method: "POST",
          body: formData,
        })
        if (resp.ok) {
          const result = await resp.json()
          imageUrl = result.url
        }
      } finally {
        setIsUploading(false)
      }
    }

    let actualCategoryId = data.category_id

    if (isCustomCategory && data.custom_category) {
      const customName = data.custom_category.trim()
      if (!customName) return
      const customLower = customName.toLowerCase()
      const existing = categories.find(
        (c) => c.name.toLowerCase() === customLower,
      )
      if (existing) {
        actualCategoryId = existing.id
      } else {
        try {
          const created = await publicApi.categories.create({ name: customName })
          actualCategoryId = created.id
        } catch {
          return
        }
      }
    }

    if (actualCategoryId === "__custom__") {
      actualCategoryId = ""
    }

    const payload = {
      title: data.title,
      short_description: data.short_description || undefined,
      description: data.description,
      start_date: data.start_date,
      start_time: data.start_time || undefined,
      end_time: data.end_time || undefined,
      location: data.location,
      image_url: imageUrl || undefined,
      registration_url: data.registration_url || undefined,
      status: data.status,
      organizer_id: data.organizer_id || undefined,
      category_id: actualCategoryId || undefined,
      target_audience: data.target_audience || undefined,
      participation_enabled: data.participation_enabled,
    }

    if (isEditing && event) {
      await updateEvent.mutateAsync({ id: event.id, data: payload })
      router.push(`/dashboard/events/${event.id}`)
    } else {
      const result = await createEvent.mutateAsync(payload)
      localStorage.removeItem(FORM_STORAGE_KEY)
      router.push(`/dashboard/events/${result.id}`)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          {isEditing ? "Редактирование мероприятия" : "Создание мероприятия"}
        </CardTitle>
      </CardHeader>
      <motion.form
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        onSubmit={handleSubmit(onSubmit)}
        className="space-y-6"
      >
        {error && <Alert variant="error">{error.message}</Alert>}

        <div className="rounded-xl border border-border bg-surface-secondary p-5">
          <h3 className="mb-4 text-sm font-semibold text-foreground">
            Основная информация
          </h3>
          <div className="space-y-4">
            <Input
              label="Название"
              placeholder="Название мероприятия"
              helperText="Обязательное поле. Максимум 255 символов."
              {...register("title")}
              error={errors.title?.message}
            />
            <Textarea
              label="Описание"
              rows={5}
              placeholder="Полное описание мероприятия"
              helperText="Обязательное поле. Подробно опишите программу и условия участия."
              {...register("description")}
              error={errors.description?.message}
            />
            <Input
              label="Краткое описание"
              placeholder="Краткий анонс для карточки события (необязательно)"
              helperText="Отображается в карточке события на главной странице."
              {...register("short_description")}
              error={errors.short_description?.message}
            />
          </div>
        </div>

        <div className="rounded-xl border border-border bg-surface-secondary p-5">
          <h3 className="mb-4 text-sm font-semibold text-foreground">
            Дата и время
          </h3>
          <div className="grid gap-4 sm:grid-cols-3">
            <Input
              label="Дата начала"
              type="date"
              helperText="Обязательное поле"
              {...register("start_date")}
              error={errors.start_date?.message}
            />
            <Input
              label="Время начала"
              type="time"
              helperText="Необязательно"
              {...register("start_time")}
              error={errors.start_time?.message}
            />
            <Input
              label="Время окончания"
              type="time"
              helperText="Необязательно"
              {...register("end_time")}
              error={errors.end_time?.message}
            />
          </div>
        </div>

        <div className="rounded-xl border border-border bg-surface-secondary p-5">
          <h3 className="mb-4 text-sm font-semibold text-foreground">
            Место и ссылки
          </h3>
          <div className="space-y-4">
            <Input
              label="Место проведения"
              placeholder="Адрес или аудитория"
              helperText="Обязательное поле. Например: Главный корпус БГИТУ, ауд. 301"
              {...register("location")}
              error={errors.location?.message}
            />
            <Input
              label="Ссылка на регистрацию"
              type="url"
              placeholder="https://example.com/register"
              helperText="Оставьте пустым, если регистрация не требуется."
              {...register("registration_url")}
              error={errors.registration_url?.message}
            />
          </div>
        </div>

        <div className="rounded-xl border border-border bg-surface-secondary p-5">
          <h3 className="mb-4 text-sm font-semibold text-foreground">
            Изображение
          </h3>
          <div
            onDrop={handleDrop}
            onDragOver={(e) => e.preventDefault()}
            onClick={() => fileInputRef.current?.click()}
            className="flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-border bg-white p-8 transition-colors hover:border-primary-400 hover:bg-primary-50/50"
          >
            {imagePreview ? (
              <div className="relative w-full max-w-md">
                <Image
                  src={getImageUrl(imagePreview)}
                  alt="Preview"
                  width={400}
                  height={225}
                  className="h-48 w-full rounded-lg object-cover"
                />
                <div className="mt-3 flex justify-center gap-2">
                  <Button
                    type="button"
                    variant="secondary"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation()
                      fileInputRef.current?.click()
                    }}
                  >
                    <Upload className="mr-1 h-3 w-3" />
                    Заменить
                  </Button>
                  <Button
                    type="button"
                    variant="danger"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation()
                      removeImage()
                    }}
                  >
                    <Trash2 className="mr-1 h-3 w-3" />
                    Удалить
                  </Button>
                </div>
              </div>
            ) : (
              <>
                <ImagePlus className="mb-2 h-10 w-10 text-foreground-muted" />
                <p className="text-sm font-medium text-foreground">
                  Перетащите изображение сюда или нажмите для выбора
                </p>
                <p className="mt-1 text-xs text-foreground-muted">
                  JPG, PNG, WebP до 10 МБ
                </p>
              </>
            )}
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => {
              const file = e.target.files?.[0]
              if (file) handleImageSelected(file)
            }}
          />
          <input type="hidden" {...register("image_url")} />
        </div>

        <div className="rounded-xl border border-border bg-surface-secondary p-5">
          <h3 className="mb-4 text-sm font-semibold text-foreground">
            Категория и аудитория
          </h3>
          <div className="space-y-4">
            <Select
              label="Категория"
              options={categoryOptions}
              helperText="Выберите тип мероприятия"
              {...register("category_id")}
              error={errors.category_id?.message}
            />
            {isCustomCategory && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
              >
                <Input
                  label="Название категории"
                  placeholder="Введите название категории"
                  helperText="Эта категория будет отображаться на карточке события."
                  {...register("custom_category")}
                  error={errors.custom_category?.message}
                />
              </motion.div>
            )}
            <Select
              label="Целевая аудитория"
              options={TARGET_AUDIENCE_OPTIONS}
              helperText="Для кого предназначено мероприятие"
              {...register("target_audience")}
              error={errors.target_audience?.message}
            />
          </div>
        </div>

        <div className="rounded-xl border border-border bg-surface-secondary p-5">
          <h3 className="mb-4 text-sm font-semibold text-foreground">
            Настройки публикации
          </h3>
          <div className="space-y-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <Select
                label="Статус"
                options={STATUS_OPTIONS}
                helperText="Опубликовано — видно всем посетителям"
                {...register("status")}
                error={errors.status?.message}
              />
              <Select
                label="Организатор"
                options={organizers.map((o) => ({
                  value: o.id,
                  label: o.name,
                }))}
                helperText={
                  isAdmin
                    ? "Выберите организатора из списка"
                    : "Организатор назначается автоматически"
                }
                {...register("organizer_id")}
                error={errors.organizer_id?.message}
              />
            </div>
            <div className="flex items-center gap-3 rounded-xl border border-border bg-white p-4">
              <Controller
                name="participation_enabled"
                control={control}
                render={({ field }) => (
                  <label className="flex cursor-pointer items-center gap-3">
                    <input
                      type="checkbox"
                      checked={field.value ?? true}
                      onChange={(e) => field.onChange(e.target.checked)}
                      className="h-5 w-5 rounded border-border text-primary-600 focus:ring-primary-500"
                    />
                    <div>
                      <span className="text-sm font-medium text-foreground">
                        Разрешить запись на мероприятие
                      </span>
                      <p className="text-xs text-foreground-muted flex items-center gap-1">
                        <Info className="h-3 w-3" />
                        Посетители смогут отметить «Буду участвовать»
                      </p>
                    </div>
                  </label>
                )}
              />
            </div>
          </div>
        </div>

        <div className="flex gap-3 pt-2">
          <Button type="submit" isLoading={isSubmitting || isUploading}>
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
