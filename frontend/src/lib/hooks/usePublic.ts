"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { publicApi } from "@/lib/api/public"

export function useCategories() {
  return useQuery({
    queryKey: ["categories"],
    queryFn: () => publicApi.categories.list(),
    staleTime: 5 * 60 * 1000,
  })
}

export function usePublicEvents(params?: { offset?: number; limit?: number; search?: string; date_from?: string; date_to?: string }) {
  return useQuery({
    queryKey: ["public-events", params],
    queryFn: () => publicApi.events.list({ ...params, status: "published" }),
  })
}

export function usePublicEvent(id: string | undefined) {
  return useQuery({
    queryKey: ["public-event", id],
    queryFn: () => publicApi.events.getById(id!),
    enabled: !!id,
  })
}

export function useParticipationStatus(eventId: string | undefined) {
  return useQuery({
    queryKey: ["participation", eventId],
    queryFn: () => publicApi.participation.status(eventId!),
    enabled: !!eventId,
    retry: false,
  })
}

export function useRegisterParticipation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (eventId: string) => publicApi.participation.register(eventId),
    onSuccess: (_, eventId) => {
      queryClient.invalidateQueries({ queryKey: ["participation", eventId] })
      queryClient.invalidateQueries({ queryKey: ["public-events"] })
      queryClient.invalidateQueries({ queryKey: ["public-event", eventId] })
    },
  })
}

export function useCancelParticipation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (eventId: string) => publicApi.participation.cancel(eventId),
    onSuccess: (_, eventId) => {
      queryClient.invalidateQueries({ queryKey: ["participation", eventId] })
      queryClient.invalidateQueries({ queryKey: ["public-events"] })
      queryClient.invalidateQueries({ queryKey: ["public-event", eventId] })
    },
  })
}
