"use client"

import { useQuery, useMutation } from "@tanstack/react-query"
import { publicApi } from "@/lib/api/public"

export function useCategories() {
  return useQuery({
    queryKey: ["categories"],
    queryFn: () => publicApi.categories.list(),
    staleTime: 5 * 60 * 1000,
  })
}

export function usePublicEvents(params?: { offset?: number; limit?: number; search?: string; date_from?: string; date_to?: string }) {
  const today = new Date().toISOString().slice(0, 10)
  return useQuery({
    queryKey: ["public-events", params],
    queryFn: () => publicApi.events.list({ ...params, status: "published", date_from: params?.date_from ?? today }),
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
    staleTime: 30_000,
  })
}

export function useRegisterParticipation() {
  return useMutation({
    mutationFn: (eventId: string) => publicApi.participation.register(eventId),
  })
}

export function useCancelParticipation() {
  return useMutation({
    mutationFn: (eventId: string) => publicApi.participation.cancel(eventId),
  })
}
