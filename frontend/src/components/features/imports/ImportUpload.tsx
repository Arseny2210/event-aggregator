"use client"

import { useState, useRef } from "react"
import { useRouter } from "next/navigation"
import { motion } from "framer-motion"
import { Upload } from "lucide-react"
import { Button } from "@/components/ui/Button"
import { Card, CardHeader, CardTitle } from "@/components/ui/Card"
import { Alert } from "@/components/ui/Alert"
import { useUploadImport } from "@/lib/hooks/useImports"

export function ImportUpload() {
  const router = useRouter()
  const fileRef = useRef<HTMLInputElement>(null)
  const [file, setFile] = useState<File | null>(null)
  const upload = useUploadImport()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return
    const result = await upload.mutateAsync(file)
    router.push(`/dashboard/imports/${result.id}`)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Загрузка файла</CardTitle>
      </CardHeader>
      <motion.form
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        onSubmit={handleSubmit}
        className="space-y-4"
      >
        {upload.error && (
          <Alert variant="error">{upload.error.message}</Alert>
        )}

        <div
          className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-border p-8 transition-all hover:border-primary-400 hover:bg-primary-50/50"
          onClick={() => fileRef.current?.click()}
        >
          <Upload className="mb-3 h-10 w-10 text-foreground-muted" />
          <p className="text-sm font-medium text-foreground">
            {file ? file.name : "Нажмите для выбора Excel-файла"}
          </p>
          <p className="mt-1 text-xs text-foreground-muted">
            Формат .xlsx или .xls
          </p>
          <input
            ref={fileRef}
            type="file"
            accept=".xlsx,.xls"
            className="hidden"
            onChange={(e) => {
              const f = e.target.files?.[0]
              if (f) setFile(f)
            }}
          />
        </div>

        <div className="flex gap-3">
          <Button type="submit" disabled={!file} isLoading={upload.isPending}>
            Загрузить
          </Button>
          <Button
            type="button"
            variant="secondary"
            onClick={() => router.back()}
          >
            Отмена
          </Button>
        </div>
      </motion.form>
    </Card>
  )
}
