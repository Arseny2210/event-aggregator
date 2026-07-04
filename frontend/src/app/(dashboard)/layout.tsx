import { Sidebar } from "@/components/layout/Sidebar"
import { DashboardHeader } from "@/components/features/dashboard/DashboardHeader"

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden lg:ml-0">
        <DashboardHeader />
        <main className="flex-1 overflow-y-auto bg-slate-50 p-4 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  )
}
