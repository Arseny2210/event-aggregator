"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { notificationsApi } from "@/lib/api/notifications"
import type {
  NotifListParams,
  SendNotificationDto,
  SendTestNotificationDto,
} from "@/types/notifications"

export function useNotifications(params?: NotifListParams) {
  return useQuery({
    queryKey: ["notifications", params],
    queryFn: () => notificationsApi.list(params),
  })
}

export function useNotification(id: string | undefined) {
  return useQuery({
    queryKey: ["notifications", id],
    queryFn: () => notificationsApi.getById(id!),
    enabled: !!id,
  })
}

export function useSendNotification() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: SendNotificationDto) => notificationsApi.send(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notifications"] })
    },
  })
}

export function useSendTestNotification() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: SendTestNotificationDto) => notificationsApi.sendTest(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notifications"] })
    },
  })
}

export function useNotificationTemplates(params?: { offset?: number; limit?: number }) {
  return useQuery({
    queryKey: ["notifications", "templates", params],
    queryFn: () => notificationsApi.listTemplates(params),
  })
}
