"use client"

import { useQuery } from "@tanstack/react-query"
import { organizersApi } from "@/lib/api/organizers"

export function useOrganizers() {
  return useQuery({
    queryKey: ["organizers"],
    queryFn: () => organizersApi.list(),
    staleTime: 10 * 60 * 1000,
  })
}
