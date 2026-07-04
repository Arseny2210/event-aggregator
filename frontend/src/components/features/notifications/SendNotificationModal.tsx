"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Modal } from "@/components/ui/Modal"
import { Input } from "@/components/ui/Input"
import { Select } from "@/components/ui/Select"
import { Button } from "@/components/ui/Button"
import { Alert } from "@/components/ui/Alert"
import { useSendNotification } from "@/lib/hooks/useNotifications"
import type { NotificationChannelType, NotificationPriority, NotificationTemplateType } from "@/types/notifications"

const schema = z.object({
  channel: z.enum(["email", "telegram", "in_app"]),
  recipient: z.string().min(1, "Required").max(500),
  template_type: z.enum(["welcome", "password_reset", "event_published", "event_reminder", "import_completed", "import_failed"]),
  priority: z.enum(["low", "normal", "high", "critical"]),
  context: z.string().optional(),
  language: z.string().optional(),
})

type FormData = z.infer<typeof schema>

const CHANNEL_OPTIONS = [
  { value: "email", label: "Email" },
  { value: "telegram", label: "Telegram" },
  { value: "in_app", label: "In-App" },
]
const TEMPLATE_OPTIONS = [
  { value: "welcome", label: "Welcome" },
  { value: "password_reset", label: "Password Reset" },
  { value: "event_published", label: "Event Published" },
  { value: "event_reminder", label: "Event Reminder" },
  { value: "import_completed", label: "Import Completed" },
  { value: "import_failed", label: "Import Failed" },
]
const PRIORITY_OPTIONS = [
  { value: "low", label: "Low" },
  { value: "normal", label: "Normal" },
  { value: "high", label: "High" },
  { value: "critical", label: "Critical" },
]

interface SendNotificationModalProps {
  open: boolean
  onClose: () => void
}

export function SendNotificationModal({ open, onClose }: SendNotificationModalProps) {
  const sendNotif = useSendNotification()
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: { channel: "email", template_type: "welcome", priority: "normal", language: "en" },
  })

  const onSubmit = async (data: FormData) => {
    let context: Record<string, unknown> = {}
    if (data.context) {
      try { context = JSON.parse(data.context) } catch { return }
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
    <Modal open={open} onClose={onClose} title="Send Notification">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {sendNotif.error && <Alert variant="error">{sendNotif.error.message}</Alert>}

        <Select label="Channel" options={CHANNEL_OPTIONS} {...register("channel")} error={errors.channel?.message} />
        <Input label="Recipient" placeholder="user@example.com" {...register("recipient")} error={errors.recipient?.message} />
        <Select label="Template" options={TEMPLATE_OPTIONS} {...register("template_type")} error={errors.template_type?.message} />
        <Select label="Priority" options={PRIORITY_OPTIONS} {...register("priority")} error={errors.priority?.message} />
        <div>
          <label className="mb-1 block text-sm font-medium text-slate-700">Context (JSON)</label>
          <textarea
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            rows={4}
            placeholder='{"key": "value"}'
            {...register("context")}
          />
        </div>

        <div className="flex justify-end gap-3">
          <Button variant="secondary" type="button" onClick={onClose}>Cancel</Button>
          <Button type="submit" isLoading={isSubmitting || sendNotif.isPending}>Send</Button>
        </div>
      </form>
    </Modal>
  )
}
