"use client"

import { useParams } from "next/navigation"
import { ImportDetail } from "@/components/features/imports/ImportDetail"

export default function ImportDetailPage() {
  const { id } = useParams<{ id: string }>()
  return <ImportDetail importId={id} />
}
