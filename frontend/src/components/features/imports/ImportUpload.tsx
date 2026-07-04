"use client"

import { useState, useRef } from "react"
import { useRouter } from "next/navigation"
import { Upload } from "lucide-react"
import { Button } from "@/components/ui/Button"
import { Card } from "@/components/ui/Card"
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
      <form onSubmit={handleSubmit} className="space-y-4">
        {upload.error && <Alert variant="error">{upload.error.message}</Alert>}

        <div
          className="flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-slate-300 p-8 transition-colors hover:border-blue-400"
          onClick={() => fileRef.current?.click()}
        >
          <Upload className="mb-3 h-10 w-10 text-slate-400" />
          <p className="text-sm font-medium text-slate-700">
            {file ? file.name : "Click to select an Excel file"}
          </p>
          <p className="mt-1 text-xs text-slate-500">.xlsx or .xls format</p>
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
            Upload
          </Button>
          <Button type="button" variant="secondary" onClick={() => router.back()}>
            Cancel
          </Button>
        </div>
      </form>
    </Card>
  )
}
