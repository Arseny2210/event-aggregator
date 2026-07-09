"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { publicNotificationsApi } from "@/lib/api/public-notifications"

export function usePublicNotifications(sessionId: string | undefined) {
  return useQuery({
    queryKey: ["public-notifications", sessionId],
    queryFn: () => publicNotificationsApi.list(sessionId!),
    enabled: !!sessionId,
    refetchInterval: 15_000,
  })
}

export function useMarkNotificationAsRead() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ notificationId, sessionId }: { notificationId: string; sessionId: string }) =>
      publicNotificationsApi.markAsRead(notificationId, sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["public-notifications"] })
    },
  })
}

export function useDeleteNotification() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ notificationId, sessionId }: { notificationId: string; sessionId: string }) =>
      publicNotificationsApi.delete(notificationId, sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["public-notifications"] })
    },
  })
}
