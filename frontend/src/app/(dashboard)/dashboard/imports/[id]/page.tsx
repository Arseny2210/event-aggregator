"use client"

import { useParams } from "next/navigation"
import { PageTransition } from "@/components/motion/PageTransition"
import { ImportDetail } from "@/components/features/imports/ImportDetail"

export default function ImportDetailPage() {
  const { id } = useParams<{ id: string }>()
  return (
    <PageTransition>
      <ImportDetail importId={id} />
    </PageTransition>
  )
}
