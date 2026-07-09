"use client"

import { useQuery } from "@tanstack/react-query"
import { apiClient } from "@/lib/api/client"

function fetchSessionId(): Promise<string> {
  return apiClient
    .get<{ session_id: string }>("/session/")
    .then((r) => r.session_id)
    .catch(() => "")
}

export function useSessionId(): string | undefined {
  const { data } = useQuery({
    queryKey: ["session-id"],
    queryFn: fetchSessionId,
    staleTime: Infinity,
    gcTime: Infinity,
  })
  return data || undefined
}
