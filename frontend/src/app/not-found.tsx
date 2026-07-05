import Link from "next/link"
import { Button } from "@/components/ui/Button"
import { GraduationCap, Home } from "lucide-react"

export default function NotFoundPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-primary-950 to-primary-900 px-4">
      <div className="flex flex-col items-center text-center">
        <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-white/10 backdrop-blur-sm">
          <GraduationCap className="h-8 w-8 text-white" />
        </div>
        <h1 className="mb-2 text-8xl font-bold text-white">404</h1>
        <p className="mb-2 text-xl text-blue-200/80">
          Страница не найдена
        </p>
        <p className="mb-8 text-sm text-blue-200/50">
          Запрашиваемая страница не существует или была перемещена
        </p>
        <Link href="/">
          <Button
            variant="primary"
            size="lg"
            className="bg-white text-primary-900 hover:bg-blue-50"
          >
            <Home className="mr-2 h-4 w-4" />
            На главную
          </Button>
        </Link>
      </div>
    </div>
  )
}
