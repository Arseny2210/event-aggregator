"use client"

import { PageTransition } from "@/components/motion/PageTransition"
import { DashboardCard } from "@/components/features/dashboard/DashboardCard"
import { RecentActivity } from "@/components/features/dashboard/RecentActivity"
import { QuickActions } from "@/components/features/dashboard/QuickActions"
import { Calendar, Bell, Upload, Activity } from "lucide-react"
import { useEvents } from "@/lib/hooks/useEvents"
import { useImports } from "@/lib/hooks/useImports"
import { useAuth } from "@/lib/hooks/useAuth"

export default function DashboardPage() {
  const { user } = useAuth()
  const { data: eventsData } = useEvents({ limit: 1 })
  const { data: importsData } = useImports({ limit: 1 })

  const totalEvents = eventsData?.total ?? 0
  const totalImports = importsData?.total ?? 0

  return (
    <PageTransition>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">
            С возвращением, {user?.email?.split("@")[0] ?? "пользователь"}
          </h1>
          <p className="mt-1 text-sm text-foreground-secondary">
            Панель управления информационной системой
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <DashboardCard
            title="Мероприятия"
            value={totalEvents}
            description="Всего в системе"
            icon={Calendar}
            color="blue"
          />
          <DashboardCard
            title="Импорты"
            value={totalImports}
            description="Всего загружено"
            icon={Upload}
            color="green"
          />
          <DashboardCard
            title="Уведомления"
            value="—"
            description="За всё время"
            icon={Bell}
            color="amber"
          />
          <DashboardCard
            title="Активность"
            value="—"
            description="Сегодня"
            icon={Activity}
            color="purple"
          />
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <RecentActivity />
          <QuickActions />
        </div>
      </div>
    </PageTransition>
  )
}
