"use client"

import { useState } from "react"
import Link from "next/link"
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
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-900">Imports</h1>
        {canUpload && (
          <Link href="/dashboard/imports/new">
            <Button>
              <Upload className="mr-1 h-4 w-4" />
              Upload
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
  )
}
