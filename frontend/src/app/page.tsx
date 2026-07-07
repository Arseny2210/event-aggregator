"use client"

import { useState, useMemo, useCallback, useRef, useEffect } from "react"
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
import { DEFAULT_CATEGORIES } from "@/types/categories"

const VIEW_TABS = [
  { id: "timeline", label: "Лента" },
  { id: "calendar", label: "Календарь" },
]

const CATEGORY_ALL = { value: "", label: "Все категории" }
const CATEGORY_OTHER_VALUE = "__other__"
const CATEGORY_OTHER = { value: CATEGORY_OTHER_VALUE, label: "Другая" }
const DEFAULT_CATEGORY_NAMES = new Set(DEFAULT_CATEGORIES.map((n) => n.toLowerCase()))

export default function HomePage() {
  const [view, setView] = useState("timeline")
  const [searchInput, setSearchInput] = useState("")
  const [debouncedSearch, setDebouncedSearch] = useState("")
  const [categoryFilter, setCategoryFilter] = useState("")
  const debounceRef = useRef<NodeJS.Timeout | null>(null)

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => {
      setDebouncedSearch(searchInput.trim().replace(/\s+/g, " "))
    }, 500)
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current)
    }
  }, [searchInput])

  const { data: categoriesData } = useCategories()
  const { data: eventsData, isLoading, isFetching } = usePublicEvents({
    limit: 100,
    search: debouncedSearch || undefined,
  })

  const { categoryOptions, knownCategoryIds } = useMemo(() => {
    const cats = categoriesData ?? []
    const defaults: { value: string; label: string }[] = []
    let hasOther = false
    const knownIds: string[] = []
    for (const c of cats) {
      if (DEFAULT_CATEGORY_NAMES.has(c.name.toLowerCase())) {
        defaults.push({ value: c.id, label: c.name })
        knownIds.push(c.id)
      } else {
        hasOther = true
      }
    }
    const options = [CATEGORY_ALL, ...defaults]
    if (hasOther) {
      options.push(CATEGORY_OTHER)
    }
    return { categoryOptions: options, knownCategoryIds: knownIds }
  }, [categoriesData])

  const events = useMemo(() => {
    const all = eventsData?.items ?? []
    if (!categoryFilter) return all
    if (categoryFilter === CATEGORY_OTHER_VALUE) {
      return all.filter((e) => !knownCategoryIds.includes(e.category_id))
    }
    return all.filter((e) => e.category_id === categoryFilter)
  }, [eventsData, categoryFilter, knownCategoryIds])

  const totalEvents = eventsData?.total ?? 0
  const hasMore = !categoryFilter && events.length < totalEvents

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

              <div className="flex flex-col-reverse gap-3 sm:flex-row sm:items-center">
                <div className="relative w-full sm:w-64">
                  <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-foreground-muted" />
                  <Input
                    placeholder="Поиск мероприятий..."
                    value={searchInput}
                    onChange={(e) => setSearchInput(e.target.value)}
                    className="pl-9 w-full"
                  />
                </div>
                <Select
                  options={categoryOptions}
                  value={categoryFilter}
                  onChange={(e) => setCategoryFilter(e.target.value)}
                  className="w-full sm:w-48"
                />
              </div>
            </motion.div>

            {isLoading ? (
              <div className="flex items-center justify-center py-16">
                <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary-500 border-t-transparent" />
              </div>
            ) : (
              <motion.div
                key={view}
                initial={{ opacity: 0, x: view === "calendar" ? 20 : -20 }}
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
