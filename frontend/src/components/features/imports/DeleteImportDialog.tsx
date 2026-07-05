"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Trash2 } from "lucide-react"
import { Button } from "@/components/ui/Button"
import { Modal } from "@/components/ui/Modal"
import { Alert } from "@/components/ui/Alert"
import { useDeleteImport } from "@/lib/hooks/useImports"

interface DeleteImportButtonProps {
  importId: string
  importFilename: string
}

export function DeleteImportButton({
  importId,
  importFilename,
}: DeleteImportButtonProps) {
  const [open, setOpen] = useState(false)
  const router = useRouter()
  const deleteImport = useDeleteImport()

  const handleDelete = async () => {
    await deleteImport.mutateAsync(importId)
    setOpen(false)
    router.push("/dashboard/imports")
  }

  return (
    <>
      <Button variant="danger" size="sm" onClick={() => setOpen(true)}>
        <Trash2 className="mr-1 h-4 w-4" />
        Удалить
      </Button>
      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title="Удаление импорта"
      >
        <div className="space-y-4">
          {deleteImport.error && (
            <Alert variant="error">{deleteImport.error.message}</Alert>
          )}
          <p className="text-sm text-foreground-secondary">
            Удалить{" "}
            <strong className="text-foreground">{importFilename}</strong>? Это
            действие нельзя отменить.
          </p>
          <div className="flex justify-end gap-3">
            <Button variant="secondary" onClick={() => setOpen(false)}>
              Отмена
            </Button>
            <Button
              variant="danger"
              onClick={handleDelete}
              isLoading={deleteImport.isPending}
            >
              Удалить
            </Button>
          </div>
        </div>
      </Modal>
    </>
  )
}
