"use client"

import { useState } from "react"
import Link from "next/link"
import { PageTransition } from "@/components/motion/PageTransition"
import { Upload } from "lucide-react"
import { Button } from "@/components/ui/Button"
import { ImportList } from "@/components/features/imports/ImportList"
import { useAuth } from "@/lib/hooks/useAuth"

export default function ImportsPage() {
  const { user } = useAuth()
  const canUpload = user?.permissions?.includes("import:create")
  const [offset, setOffset] = useState(0)
  const [status, setStatus] = useState("")
  const limit = 20

  return (
    <PageTransition>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground">
              Импорт данных
            </h1>
            <p className="text-sm text-foreground-secondary">
              Загрузка и обработка файлов с мероприятиями
            </p>
          </div>
          {canUpload && (
            <Link href="/dashboard/imports/new">
              <Button>
                <Upload className="mr-1 h-4 w-4" />
                Загрузить
              </Button>
            </Link>
          )}
        </div>
        <ImportList
          offset={offset}
          limit={limit}
          status={status}
          onPageChange={setOffset}
          onStatusChange={setStatus}
        />
      </div>
    </PageTransition>
  )
}
