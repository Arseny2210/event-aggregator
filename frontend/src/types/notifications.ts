export type NotificationStatus = "pending" | "sent" | "failed" | "retrying"

export type NotificationChannelType = "email" | "telegram" | "in_app"

export type NotificationPriority = "low" | "normal" | "high" | "critical"

export type NotificationTemplateType =
  | "welcome"
  | "password_reset"
  | "event_published"
  | "event_reminder"
  | "import_completed"
  | "import_failed"

export interface Notification {
  id: string
  channel: NotificationChannelType
  recipient: string
  template_type: NotificationTemplateType
  payload: Record<string, unknown>
  subject?: string
  status: NotificationStatus
  priority: NotificationPriority
  attempts: number
  error_message?: string
  created_at: string
  sent_at?: string
  scheduled_at?: string
  read_at?: string
  deleted_at?: string
  event_id?: string
}

export interface NotifListParams {
  offset?: number
  limit?: number
  status?: NotificationStatus
}

export interface SendNotificationDto {
  channel: NotificationChannelType
  recipient: string
  template_type: NotificationTemplateType
  priority?: NotificationPriority
  context: Record<string, unknown>
  language?: string
}

export interface SendTestNotificationDto {
  channel: NotificationChannelType
  recipient: string
  template_type: NotificationTemplateType
  language?: string
}

export const NOTIF_STATUS_LABELS: Record<NotificationStatus, string> = {
  pending: "Ожидание",
  sent: "Отправлено",
  failed: "Ошибка",
  retrying: "Повтор",
}

export const NOTIF_STATUS_COLORS: Record<NotificationStatus, string> = {
  pending: "bg-slate-100 text-slate-700",
  sent: "bg-green-100 text-green-700",
  failed: "bg-red-100 text-red-700",
  retrying: "bg-amber-100 text-amber-700",
}

export const NOTIF_PRIORITY_LABELS: Record<NotificationPriority, string> = {
  low: "Низкий",
  normal: "Обычный",
  high: "Высокий",
  critical: "Критический",
}

export const NOTIF_PRIORITY_COLORS: Record<NotificationPriority, string> = {
  low: "bg-slate-100 text-slate-700",
  normal: "bg-blue-100 text-blue-700",
  high: "bg-amber-100 text-amber-700",
  critical: "bg-red-100 text-red-700",
}

export const NOTIF_CHANNEL_LABELS: Record<NotificationChannelType, string> = {
  email: "Email",
  telegram: "Telegram",
  in_app: "В приложении",
}

export const NOTIF_TEMPLATE_LABELS: Record<NotificationTemplateType, string> = {
  welcome: "Приветствие",
  password_reset: "Сброс пароля",
  event_published: "Мероприятие опубликовано",
  event_reminder: "Напоминание о мероприятии",
  import_completed: "Импорт завершён",
  import_failed: "Ошибка импорта",
}
