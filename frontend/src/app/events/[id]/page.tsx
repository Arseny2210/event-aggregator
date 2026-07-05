"use client"

import { useParams } from "next/navigation"
import { PublicEventDetail } from "@/components/features/public/PublicEventDetail"
import { Header } from "@/components/layout/Header"
import { Footer } from "@/components/layout/Footer"

export default function PublicEventPage() {
  const { id } = useParams<{ id: string }>()
  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1 bg-surface-secondary">
        <div className="mx-auto max-w-4xl px-4 py-12">
          <PublicEventDetail eventId={id} />
        </div>
      </main>
      <Footer />
    </div>
  )
}
