"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { importsApi } from "@/lib/api/imports"
import type { ImportListParams, RowResultParams } from "@/types/imports"

export function useImports(params?: ImportListParams) {
  return useQuery({
    queryKey: ["imports", params],
    queryFn: () => importsApi.list(params),
  })
}

export function useImport(id: string | undefined) {
  return useQuery({
    queryKey: ["imports", id],
    queryFn: () => importsApi.getById(id!),
    enabled: !!id,
    refetchInterval: (query) =>
      query.state.data?.status === "processing" ? 2000 : false,
  })
}

export function useImportRows(id: string | undefined, params?: RowResultParams) {
  return useQuery({
    queryKey: ["imports", id, "rows", params],
    queryFn: () => importsApi.getRows(id!, params),
    enabled: !!id,
  })
}

export function useUploadImport() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (file: File) => importsApi.upload(file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["imports"] })
    },
  })
}

export function useDeleteImport() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => importsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["imports"] })
    },
  })
}
