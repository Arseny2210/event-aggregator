"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Modal } from "@/components/ui/Modal"
import { Input } from "@/components/ui/Input"
import { Textarea } from "@/components/ui/Textarea"
import { Select } from "@/components/ui/Select"
import { Button } from "@/components/ui/Button"
import { Alert } from "@/components/ui/Alert"
import { useSendNotification } from "@/lib/hooks/useNotifications"
import type {
  NotificationChannelType,
  NotificationPriority,
  NotificationTemplateType,
} from "@/types/notifications"

const schema = z.object({
  channel: z.enum(["email", "telegram", "in_app"]),
  recipient: z.string().min(1, "Обязательное поле").max(500),
  template_type: z.enum([
    "welcome",
    "password_reset",
    "event_published",
    "event_reminder",
    "import_completed",
    "import_failed",
  ]),
  priority: z.enum(["low", "normal", "high", "critical"]),
  context: z.string().optional(),
  language: z.string().optional(),
})

type FormData = z.infer<typeof schema>

const CHANNEL_OPTIONS = [
  { value: "email", label: "Email" },
  { value: "telegram", label: "Telegram" },
  { value: "in_app", label: "В приложении" },
]
const TEMPLATE_OPTIONS = [
  { value: "welcome", label: "Приветствие" },
  { value: "password_reset", label: "Сброс пароля" },
  { value: "event_published", label: "Мероприятие опубликовано" },
  { value: "event_reminder", label: "Напоминание" },
  { value: "import_completed", label: "Импорт завершён" },
  { value: "import_failed", label: "Ошибка импорта" },
]
const PRIORITY_OPTIONS = [
  { value: "low", label: "Низкий" },
  { value: "normal", label: "Обычный" },
  { value: "high", label: "Высокий" },
  { value: "critical", label: "Критический" },
]

interface SendNotificationModalProps {
  open: boolean
  onClose: () => void
}

export function SendNotificationModal({
  open,
  onClose,
}: SendNotificationModalProps) {
  const sendNotif = useSendNotification()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      channel: "email",
      template_type: "welcome",
      priority: "normal",
      language: "ru",
    },
  })

  const onSubmit = async (data: FormData) => {
    let context: Record<string, unknown> = {}
    if (data.context) {
      try {
        context = JSON.parse(data.context)
      } catch {
        return
      }
    }
    await sendNotif.mutateAsync({
      channel: data.channel as NotificationChannelType,
      recipient: data.recipient,
      template_type: data.template_type as NotificationTemplateType,
      priority: data.priority as NotificationPriority,
      context,
      language: data.language,
    })
    reset()
    onClose()
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Отправка уведомления"
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {sendNotif.error && (
          <Alert variant="error">{sendNotif.error.message}</Alert>
        )}

        <Select
          label="Канал"
          options={CHANNEL_OPTIONS}
          {...register("channel")}
          error={errors.channel?.message}
        />
        <Input
          label="Получатель"
          placeholder="user@example.com"
          {...register("recipient")}
          error={errors.recipient?.message}
        />
        <Select
          label="Шаблон"
          options={TEMPLATE_OPTIONS}
          {...register("template_type")}
          error={errors.template_type?.message}
        />
        <Select
          label="Приоритет"
          options={PRIORITY_OPTIONS}
          {...register("priority")}
          error={errors.priority?.message}
        />
        <Textarea
          label="Контекст (JSON)"
          rows={4}
          placeholder='{"key": "value"}'
          {...register("context")}
        />

        <div className="flex justify-end gap-3">
          <Button variant="secondary" type="button" onClick={onClose}>
            Отмена
          </Button>
          <Button
            type="submit"
            isLoading={isSubmitting || sendNotif.isPending}
          >
            Отправить
          </Button>
        </div>
      </form>
    </Modal>
  )
}
