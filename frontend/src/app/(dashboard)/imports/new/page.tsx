"use client"

import { ImportUpload } from "@/components/features/imports/ImportUpload"

export default function NewImportPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Upload Import</h1>
      <ImportUpload />
    </div>
  )
}
