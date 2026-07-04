"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { eventsApi } from "@/lib/api/events"
import type {
  CreateEventDto,
  EventSearchParams,
  UpdateEventDto,
} from "@/types/events"

export function useEvents(params?: EventSearchParams) {
  return useQuery({
    queryKey: ["events", params],
    queryFn: () => eventsApi.list(params),
  })
}

export function useEvent(id: string | undefined) {
  return useQuery({
    queryKey: ["events", id],
    queryFn: () => eventsApi.getById(id!),
    enabled: !!id,
  })
}

export function useCreateEvent() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: CreateEventDto) => eventsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["events"] })
    },
  })
}

export function useUpdateEvent() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateEventDto }) =>
      eventsApi.update(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ["events"] })
      queryClient.invalidateQueries({ queryKey: ["events", id] })
    },
  })
}

export function useDeleteEvent() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => eventsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["events"] })
    },
  })
}
