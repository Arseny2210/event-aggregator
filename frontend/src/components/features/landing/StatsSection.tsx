"use client"

import { FadeIn } from "@/components/motion/FadeIn"
import { motion } from "framer-motion"
import { usePublicEvents } from "@/lib/hooks/usePublic"
import { useEffect, useState } from "react"
import { CalendarCheck, Users, Calendar, Activity } from "lucide-react"

function AnimatedCounter({ target, suffix }: { target: number; suffix: string }) {
  const [count, setCount] = useState(0)
  useEffect(() => {
    if (target === 0) return
    let start = 0
    const duration = 2000
    const step = Math.ceil(target / (duration / 16))
    const timer = setInterval(() => {
      start += step
      if (start >= target) {
        setCount(target)
        clearInterval(timer)
      } else {
        setCount(start)
      }
    }, 16)
    return () => clearInterval(timer)
  }, [target])
  return (
    <span>
      {count.toLocaleString()}
      {suffix}
    </span>
  )
}

export function StatsSection() {
  const { data: eventsData } = usePublicEvents({ limit: 1 })
  const totalEvents = eventsData?.total ?? 0
  const totalParticipants = eventsData?.items?.reduce(
    (sum, e) => sum + (e.participants_count ?? 0),
    0,
  ) ?? 0

  const stats = [
    { icon: CalendarCheck, value: totalEvents, suffix: "", label: "Мероприятий" },
    { icon: Users, value: totalParticipants, suffix: "+", label: "Участников" },
    { icon: Calendar, value: 100, suffix: "%", label: "Охват факультетов" },
    { icon: Activity, value: 99, suffix: "%", label: "Доступность" },
  ]

  return (
    <section className="bg-gradient-to-br from-primary-900 to-primary-800 py-16">
      <div className="mx-auto max-w-6xl px-4">
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat, index) => {
            const Icon = stat.icon
            return (
              <FadeIn key={stat.label} delay={index * 0.15}>
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  className="flex flex-col items-center rounded-2xl border border-white/10 bg-white/5 p-8 text-center backdrop-blur-sm"
                >
                  <Icon className="mb-3 h-7 w-7 text-blue-300" />
                  <div className="mb-1 text-3xl font-bold text-white">
                    <AnimatedCounter target={stat.value} suffix={stat.suffix} />
                  </div>
                  <p className="text-sm text-blue-200/70">{stat.label}</p>
                </motion.div>
              </FadeIn>
            )
          })}
        </div>
      </div>
    </section>
  )
}
