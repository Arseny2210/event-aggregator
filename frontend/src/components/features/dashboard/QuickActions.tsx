"use client"

import Link from "next/link"
import { motion } from "framer-motion"
import { Card, CardHeader, CardTitle } from "@/components/ui/Card"
import { CalendarPlus, Upload } from "lucide-react"

const actions = [
  {
    href: "/dashboard/events/new",
    label: "Создать мероприятие",
    description: "Добавить новое событие",
    icon: CalendarPlus,
    color: "text-primary-600 bg-primary-50",
  },
  {
    href: "/dashboard/imports",
    label: "Импорт мероприятий",
    description: "Загрузить CSV или XLSX",
    icon: Upload,
    color: "text-green-600 bg-green-50",
  },
]

export function QuickActions() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Быстрые действия</CardTitle>
      </CardHeader>
      <div className="space-y-3">
        {actions.map((action) => {
          const Icon = action.icon
          return (
            <motion.div
              key={action.href}
              whileHover={{ x: 4 }}
              whileTap={{ scale: 0.98 }}
            >
              <Link
                href={action.href}
                className="flex items-center gap-4 rounded-xl border border-border p-4 transition-colors hover:bg-surface-secondary"
              >
                <div
                  className={`flex h-10 w-10 items-center justify-center rounded-xl ${action.color}`}
                >
                  <Icon className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-sm font-medium text-foreground">
                    {action.label}
                  </p>
                  <p className="text-xs text-foreground-muted">
                    {action.description}
                  </p>
                </div>
              </Link>
            </motion.div>
          )
        })}
      </div>
    </Card>
  )
}
