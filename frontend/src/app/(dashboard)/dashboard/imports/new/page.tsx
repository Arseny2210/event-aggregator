"use client"

import { PageTransition } from "@/components/motion/PageTransition"
import { ImportUpload } from "@/components/features/imports/ImportUpload"

export default function NewImportPage() {
  return (
    <PageTransition>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">
            Загрузка импорта
          </h1>
          <p className="text-sm text-foreground-secondary">
            Выберите Excel-файл для импорта мероприятий
          </p>
        </div>
        <ImportUpload />
      </div>
    </PageTransition>
  )
}
