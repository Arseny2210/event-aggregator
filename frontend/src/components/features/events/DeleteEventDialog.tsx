"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Trash2 } from "lucide-react"
import { Button } from "@/components/ui/Button"
import { Modal } from "@/components/ui/Modal"
import { Alert } from "@/components/ui/Alert"
import { useDeleteEvent } from "@/lib/hooks/useEvents"

interface DeleteEventButtonProps {
  eventId: string
  eventTitle: string
}

export function DeleteEventButton({
  eventId,
  eventTitle,
}: DeleteEventButtonProps) {
  const [open, setOpen] = useState(false)
  const router = useRouter()
  const deleteEvent = useDeleteEvent()

  const handleDelete = async () => {
    await deleteEvent.mutateAsync(eventId)
    setOpen(false)
    router.push("/dashboard/events")
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
        title="Удаление мероприятия"
      >
        <div className="space-y-4">
          {deleteEvent.error && (
            <Alert variant="error">{deleteEvent.error.message}</Alert>
          )}
          <p className="text-sm text-foreground-secondary">
            Вы уверены, что хотите удалить{" "}
            <strong className="text-foreground">{eventTitle}</strong>? Это
            действие нельзя отменить.
          </p>
          <div className="flex justify-end gap-3">
            <Button variant="secondary" onClick={() => setOpen(false)}>
              Отмена
            </Button>
            <Button
              variant="danger"
              onClick={handleDelete}
              isLoading={deleteEvent.isPending}
            >
              Удалить
            </Button>
          </div>
        </div>
      </Modal>
    </>
  )
}
