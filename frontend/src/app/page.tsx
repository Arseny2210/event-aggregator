"use client"

import { useState, useMemo, useCallback } from "react"
import { Header } from "@/components/layout/Header"
import { Footer } from "@/components/layout/Footer"
import { HeroSection } from "@/components/features/landing/HeroSection"
import { StatsSection } from "@/components/features/landing/StatsSection"
import { Tabs } from "@/components/ui/Tabs"
import { Input } from "@/components/ui/Input"
import { Select } from "@/components/ui/Select"
import { CalendarView } from "@/components/features/public/CalendarView"
import { TimelineView } from "@/components/features/public/TimelineView"
import { usePublicEvents, useCategories } from "@/lib/hooks/usePublic"
import { Search } from "lucide-react"
import { motion } from "framer-motion"

const VIEW_TABS = [
  { id: "calendar", label: "Календарь" },
  { id: "timeline", label: "Лента" },
]

const CATEGORY_ALL = { value: "", label: "Все категории" }

export default function HomePage() {
  const [view, setView] = useState("calendar")
  const [search, setSearch] = useState("")
  const [categoryFilter, setCategoryFilter] = useState("")

  const { data: categoriesData } = useCategories()
  const { data: eventsData, isLoading, isFetching } = usePublicEvents({
    limit: 200,
    search: search || undefined,
  })

  const categoryOptions = useMemo(() => {
    const cats = (categoriesData ?? []).map((c) => ({
      value: c.id,
      label: c.name,
    }))
    return [CATEGORY_ALL, ...cats]
  }, [categoriesData])

  const events = useMemo(() => {
    const all = eventsData?.items ?? []
    if (!categoryFilter) return all
    return all.filter((e) => e.category_id === categoryFilter)
  }, [eventsData, categoryFilter])

  const totalEvents = eventsData?.total ?? 0
  const hasMore = events.length < totalEvents

  const handleLoadMore = useCallback(() => {
    if (hasMore && !isFetching) {
      window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" })
    }
  }, [hasMore, isFetching])

  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1">
        <HeroSection />

        <section className="bg-surface-secondary py-12">
          <div className="mx-auto max-w-6xl px-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
            >
              <Tabs tabs={VIEW_TABS} activeTab={view} onTabChange={setView} />

              <div className="flex gap-3 sm:items-center">
                <div className="relative flex-1 sm:flex-initial">
                  <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-foreground-muted" />
                  <Input
                    placeholder="Поиск мероприятий..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="pl-9 w-full sm:w-64"
                  />
                </div>
                <div className="w-full sm:w-48">
                  <Select
                    options={categoryOptions}
                    value={categoryFilter}
                    onChange={(e) => setCategoryFilter(e.target.value)}
                  />
                </div>
              </div>
            </motion.div>

            {isLoading ? (
              <div className="flex items-center justify-center py-16">
                <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary-500 border-t-transparent" />
              </div>
            ) : (
              <motion.div
                key={view}
                initial={{ opacity: 0, x: view === "calendar" ? -20 : 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3 }}
              >
                {view === "calendar" ? (
                  <CalendarView events={events} />
                ) : (
                  <TimelineView
                    events={events}
                    onLoadMore={handleLoadMore}
                    hasMore={hasMore}
                    isLoadingMore={isFetching}
                  />
                )}
              </motion.div>
            )}
          </div>
        </section>

        <StatsSection />
      </main>
      <Footer />
    </div>
  )
}
