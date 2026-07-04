import Link from "next/link"
import { Button } from "@/components/ui/Button"

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b border-slate-200">
        <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <Link href="/" className="text-lg font-bold text-slate-900">
            Event Aggregator
          </Link>
          <div className="flex items-center gap-3">
            <Link href="/login">
              <Button variant="ghost" size="sm">Sign In</Button>
            </Link>
            <Link href="/dashboard">
              <Button size="sm">Dashboard</Button>
            </Link>
          </div>
        </nav>
      </header>

      <main className="flex flex-1 items-center justify-center">
        <section className="mx-auto max-w-4xl px-4 py-16 text-center">
          <h1 className="mb-4 text-4xl font-bold tracking-tight text-slate-900">
            Event Aggregator
          </h1>
          <p className="mb-8 text-lg text-slate-600">
            Discover, manage, and participate in university events.
          </p>
          <Link href="/dashboard">
            <Button size="lg">Go to Dashboard</Button>
          </Link>
        </section>
      </main>

      <footer className="border-t border-slate-200">
        <div className="mx-auto max-w-6xl px-4 py-6 text-center text-sm text-slate-500">
          &copy; {new Date().getFullYear()} Event Aggregator
        </div>
      </footer>
    </div>
  )
}
