import { Card, CardHeader, CardTitle } from "@/components/ui/Card"

export default function DashboardPage() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-900">Dashboard</h1>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Events</CardTitle>
          </CardHeader>
          <p className="text-sm text-slate-600">Manage and discover university events.</p>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Imports</CardTitle>
          </CardHeader>
          <p className="text-sm text-slate-600">Upload and process Excel event imports.</p>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Notifications</CardTitle>
          </CardHeader>
          <p className="text-sm text-slate-600">View and manage platform notifications.</p>
        </Card>
      </div>
    </div>
  )
}
