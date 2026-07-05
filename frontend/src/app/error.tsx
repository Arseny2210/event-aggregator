"use client"

import { Button } from "@/components/ui/Button"
import { GraduationCap, RefreshCw } from "lucide-react"

export default function ErrorPage({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-primary-950 to-primary-900 px-4">
      <div className="flex flex-col items-center text-center">
        <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-white/10 backdrop-blur-sm">
          <GraduationCap className="h-8 w-8 text-white" />
        </div>
        <h1 className="mb-2 text-4xl font-bold text-white">
          Что-то пошло не так
        </h1>
        <p className="mb-8 text-blue-200/80">
          Произошла непредвиденная ошибка. Пожалуйста, попробуйте снова.
        </p>
        <Button
          variant="primary"
          size="lg"
          className="bg-white text-primary-900 hover:bg-blue-50"
          onClick={reset}
        >
          <RefreshCw className="mr-2 h-4 w-4" />
          Попробовать снова
        </Button>
      </div>
    </div>
  )
}
