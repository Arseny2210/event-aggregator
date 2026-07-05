"use client"

import { motion } from "framer-motion"
import { FadeIn } from "@/components/motion/FadeIn"
import { Calendar, List, Search, UserPlus } from "lucide-react"

const features = [
  {
    icon: Calendar,
    title: "Календарь событий",
    description: "Просматривайте мероприятия в удобном календаре с навигацией по месяцам и быстрым переходом к сегодняшнему дню.",
  },
  {
    icon: List,
    title: "Лента мероприятий",
    description: "Хронологическая лента всех событий с группировкой по датам и возможностью скрыть прошедшие.",
  },
  {
    icon: Search,
    title: "Поиск и фильтры",
    description: "Быстрый поиск по названию и фильтрация по категориям для удобного поиска нужного события.",
  },
  {
    icon: UserPlus,
    title: "Участие онлайн",
    description: "Записывайтесь на мероприятия одним кликом и управляйте своим участием через личный кабинет.",
  },
]

export function FeaturesSection() {
  return (
    <section className="bg-white py-16">
      <div className="mx-auto max-w-6xl px-4">
        <FadeIn>
          <div className="mb-10 text-center">
            <h2 className="text-2xl font-bold text-foreground">Портал мероприятий</h2>
            <p className="mt-2 text-foreground-secondary">
              Всё, что нужно для поиска и участия в событиях университета
            </p>
          </div>
        </FadeIn>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <FadeIn key={feature.title} delay={index * 0.1}>
                <motion.div
                  whileHover={{ y: -3 }}
                  className="rounded-2xl border border-border bg-surface-secondary p-5 text-center shadow-sm transition-shadow hover:shadow-md"
                >
                  <div className="mx-auto mb-3 flex h-11 w-11 items-center justify-center rounded-xl bg-primary-50 text-primary-600">
                    <Icon className="h-5 w-5" />
                  </div>
                  <h3 className="mb-1.5 text-sm font-semibold text-foreground">{feature.title}</h3>
                  <p className="text-xs leading-relaxed text-foreground-secondary">{feature.description}</p>
                </motion.div>
              </FadeIn>
            )
          })}
        </div>
      </div>
    </section>
  )
}
